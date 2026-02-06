import pyotp
from zxcvbn import zxcvbn
from datetime import datetime, timedelta
from typing import Tuple, Optional
from passlib.context import CryptContext
from fastapi import HTTPException, status
from spine.db.models import DBUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def check_password_complexity(password: str) -> bool:
        """
        Gap 2: NIST 800-63B Complexity Check.
        Uses zxcvbn for entropy analysis.
        """
        if len(password) < 12:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 12 characters long."
            )
        
        results = zxcvbn(password)
        if results['score'] < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password too weak (Score: {results['score']}/4). Feedback: {results['feedback']['warning']}"
            )
        return True

    @staticmethod
    def check_lockout(user: DBUser) -> bool:
        """
        Gap 6: Account Lockout.
        Returns True if locked.
        """
        if user.locked_until and user.locked_until > datetime.utcnow():
            return True
        return False

    @staticmethod
    def handle_failed_login(user: DBUser):
        """
        Increments failure count and locks if threshold exceeded.
        """
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            return True # Locked
        return False

    @staticmethod
    def generate_mfa_secret() -> str:
        """Gap 1: Generate TOTP Secret"""
        return pyotp.random_base32()

    @staticmethod
    def verify_mfa(secret: str, code: str) -> bool:
        """Gap 1: Verify TOTP Code"""
        totp = pyotp.TOTP(secret)
        return totp.verify(code)

    @staticmethod
    def get_mfa_uri(username: str, secret: str, issuer: str = "VTE Platform") -> str:
        """Generate Provisioning URI for QR Code"""
        return pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)
