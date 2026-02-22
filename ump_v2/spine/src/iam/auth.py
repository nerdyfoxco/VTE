import pyotp
import uuid
import time
from typing import Dict, Optional, Tuple
from security.redaction_engine import RedactionEngine

class IdentityManager:
    """
    VTE Fail-Closed Identity and Access Management Core.
    Handles Multi-Tenant Registration, Session Generation, and Mandatory TOTP MFA.
    """
    
    def __init__(self, mfa_policy_path: str, signin_policy_path: str):
        self.mfa_policy = mfa_policy_path
        self.signin_policy = signin_policy_path
        
        # In-Memory DB stub for demonstration (To be wired to SQLAlchemy)
        self._user_db: Dict[str, dict] = {}
        self._mfa_challenges: Dict[str, dict] = {}
        self._sessions: Dict[str, dict] = {}

    def register_user(self, email: str, raw_password: str, full_name: str, tenant_id: str) -> dict:
        """Implements the SignUp Contract constraints."""
        # 1. Reject if already exists
        if email in self._user_db:
            raise ValueError("IDENTITY_CONFLICT: Email already registered.")
            
        # 2. Generate immutable IDs & Secrets
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        totp_secret = pyotp.random_base32()
        
        # 3. Store (Stub)
        self._user_db[email] = {
            "user_id": user_id,
            "password_hash": self._hash_stub(raw_password),
            "full_name": full_name,
            "tenant_id": tenant_id,
            "totp_secret": totp_secret,
            "mfa_enrolled": False
        }
        
        # 4. Return Enrollment Data (Fail-Closed: Must enroll MFA immediately)
        totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name=email, issuer_name="VTE Regulated OS")
        return {
            "status": "CREATED",
            "user_id": user_id,
            "action_required": "ENROLL_MFA",
            "totp_uri": totp_uri
        }

    def initiate_signin(self, email: str, raw_password: str) -> dict:
        """Implements the SignIn Contract. Returns MFA Challenge, never a Session Token directly."""
        user = self._user_db.get(email)
        if not user or user["password_hash"] != self._hash_stub(raw_password):
            # Prevents enumeration attacks
            raise ValueError("AUTH_FAILED: Invalid credentials.")
            
        mfa_token_id = f"chl_{uuid.uuid4().hex[:16]}"
        self._mfa_challenges[mfa_token_id] = {
            "email": email,
            "expires_at": time.time() + 300 # 5 minute challenge window
        }
        
        return {
            "status": "MFA_REQUIRED",
            "mfa_token_id": mfa_token_id,
            "challenge_type": "TOTP"
        }
        
    def verify_mfa(self, mfa_token_id: str, totp_code: str) -> dict:
        """Finalizes authentication via TOTP and issues the Session Token."""
        challenge = self._mfa_challenges.pop(mfa_token_id, None)
        if not challenge or time.time() > challenge["expires_at"]:
            raise ValueError("AUTH_FAILED: Challenge expired or invalid.")
            
        user = self._user_db[challenge["email"]]
        totp = pyotp.TOTP(user["totp_secret"])
        
        if not totp.verify(totp_code):
            raise ValueError("AUTH_FAILED: Invalid TOTP code.")
            
        user["mfa_enrolled"] = True # Mark verified if first time
        
        session_token = f"vte_sess_{uuid.uuid4().hex}"
        self._sessions[session_token] = {
            "user_id": user["user_id"],
            "tenant_id": user["tenant_id"],
            "issued_at": time.time()
        }
        
        return {
            "status": "AUTHENTICATED",
            "session_token": session_token,
            "tenant_id": user["tenant_id"]
        }
        
    def _hash_stub(self, pwd: str) -> str:
        # REPLACE WITH BCRYPT IN PROD
        return f"hash_v1_{pwd[::-1]}"
