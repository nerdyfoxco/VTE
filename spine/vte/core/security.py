from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
import os
from vte.core.canonicalize import canonical_json_dumps
import hashlib

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_secret_key_change_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def sign_payload(payload: Dict[str, Any]) -> str:
    """
    Signs a canonicalized payload using the system secret (HMAC).
    Returns a hex signature.
    """
    canonical_bytes = canonical_json_dumps(payload)
    # We use the SECRET_KEY to salt the hash for a simple HMAC
    # For robust usage, use hmac module, but here we just hash(content + secret) or use JWT logic.
    # Let's use a simple JWT-style signature approach or just HMAC-SHA256
    import hmac
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'), 
        canonical_bytes, 
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature(payload: Dict[str, Any], signature: str) -> bool:
    """
    Verifies the signature of the payload.
    """
    expected_signature = sign_payload(payload)
    # Constant time compare
    import hmac
    return hmac.compare_digest(expected_signature, signature)
