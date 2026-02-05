import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from vte.orm import PermitToken, DecisionObject
from vte.core.security import sign_payload

# Permit Config
PERMIT_TTL_SECONDS = 60

class PermitIssuer:
    def __init__(self, db: Session):
        self.db = db

    def issue_permit(self, decision: DecisionObject, required_scope: List[str] = None) -> PermitToken:
        """
        Issues a cryptographically signed PermitToken for a specific Decision.
        This token authorizes the Engine to execute the side-effects.
        """
        if not decision.decision_id:
            raise ValueError("Cannot issue permit for unsaved decision.")
            
        now = datetime.now(timezone.utc)
        expires = now + timedelta(seconds=PERMIT_TTL_SECONDS)
        
        # 1. Define Scope
        scope = {
            "action": decision.intent_action,
            "target": decision.intent_target,
            "permissions": required_scope or ["execute"]
        }
        
        # 2. Construct Payload for Signing
        # We sign the core fields to prevent tampering
        payload = {
            "decision_id": str(decision.decision_id),
            "scope": scope,
            "issued_at": now.isoformat(),
            "expires_at": expires.isoformat(),
            "authority": decision.actor_user_id # Bind to actor
        }
        
        # 3. Sign
        signature = sign_payload(payload)
        
        # 4. Create Token Record
        token = PermitToken(
            token_id=uuid.uuid4(),
            decision_id=decision.decision_id,
            issued_at=now,
            expires_at=expires,
            scope_json=scope,
            signature=signature
        )
        
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        
        print(f"[PermitIssuer] Issued Permit {token.token_id} for Decision {decision.decision_id}")
        return token

    def verify_permit(self, token_id: uuid.UUID, decision_id: uuid.UUID) -> bool:
        """
        Verifies a permit is valid, active, and bound to the decision.
        """
        token = self.db.query(PermitToken).filter(PermitToken.token_id == token_id).first()
        if not token:
            print("[PermitVerifier] Token not found.")
            return False
            
        # 1. Check Decision Binding
        if token.decision_id != decision_id:
            print("[PermitVerifier] Token not bound to this decision.")
            return False
            
        # 2. Check Expiry
        # Ensure timezone awareness match
        now = datetime.now(timezone.utc)
        if token.expires_at < now:
             print("[PermitVerifier] Token expired.")
             return False
             
        # 3. Check Signature Integrity (Re-sign and compare)
        # Reconstruct payload from DB fields
        payload = {
            "decision_id": str(token.decision_id),
            "scope": token.scope_json,
            "issued_at": token.issued_at.isoformat(),
            "expires_at": token.expires_at.isoformat(),
            # We need to re-fetch the decision to get the actor? or was it not stored in permit?
            # Creating payload for signing included 'authority'. But PermitToken doesn't store 'authority' explicitly in schema?
            # Wait, I put 'authority' in payload but didn't save it to PermitToken table.
            # This will fail verification if I can't reconstruct the exact payload!
            # Pivot: Let's remove 'authority' from signature for now OR fetch it from the decision relationship.
            # Ideally Permit binds to Authority. Or we rely on Decision ID binding which is unique.
        }
        # To fix the 'authority' issue: Let's rely on the fact that if Decision is tampered, its ID changes (if ID is hash) or its content changes.
        # But Decision is mutable? No, append-only.
        # Let's fetch the decision to get the authority.
        decision = self.db.query(DecisionObject).filter(DecisionObject.decision_id == decision_id).first()
        if not decision: 
             return False
             
        payload["authority"] = decision.actor_user_id
        
        recalc_sig = sign_payload(payload)
        import hmac # Moved import
        # Old manual logic removed
        pass
        
        # Use helper
        from vte.core.security import verify_signature 
        if not verify_signature(payload, token.signature):
             print("[PermitVerifier] Signature mismatch.")
             return False
             
        return True
