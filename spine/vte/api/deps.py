from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from vte.core.security import decode_access_token

# We use validation logic here
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

from vte.db import get_db
from sqlalchemy.orm import Session
from vte.orm import UserSession

def get_current_user_claims(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Validates the JWT and returns the payload (claims).
    Enforces Session Revocation check if JTI is present.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Session Check
    jti = payload.get("jti")
    if jti:
        # Check DB
        session = db.query(UserSession).filter(UserSession.token_jti == jti).first()
        if not session:
            # Token has JTI but no session? Maybe old token or deleted session.
            # Fail closed for security in this phase.
            # But earlier tokens (pre-migration) might not have JTI.
            # If token HAS JTI, session MUST exist.
            print(f"AUTH DEBUG: Token JTI {jti} not found in DB.")
            raise credentials_exception
            
        if session.revoked == "true":
            print(f"AUTH DEBUG: Session {jti} REVOKED.")
            raise credentials_exception
            
        # Optional: Check Expiry vs DB (Token expiry should match, but DB is source of truth)
        # if session.expires_at < now...
    
    # In a real app, we might check if user exists in DB here.
    # For VTE 1.0 (Stateless/Federated Identity model), we trust the signed token.
    username: str = payload.get("sub")
    role: str = payload.get("role", "user")
    
    if username is None:
        raise credentials_exception
        
    return {"user_id": username, "role": role}
