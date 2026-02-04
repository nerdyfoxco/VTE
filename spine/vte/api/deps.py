from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from vte.core.security import decode_access_token

# We use validation logic here
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user_claims(token: str = Depends(oauth2_scheme)):
    """
    Validates the JWT and returns the payload (claims).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # In a real app, we might check if user exists in DB here.
    # For VTE 1.0 (Stateless/Federated Identity model), we trust the signed token.
    username: str = payload.get("sub")
    role: str = payload.get("role", "user")
    
    if username is None:
        raise credentials_exception
        
    return {"user_id": username, "role": role}
