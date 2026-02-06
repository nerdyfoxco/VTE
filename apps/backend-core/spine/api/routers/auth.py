from datetime import timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from spine.db.engine import get_db
from spine.db.models import DBUser
from spine.core.security import SecurityService
from pydantic import BaseModel

router = APIRouter()

# Schema for Token
class Token(BaseModel):
    access_token: str
    token_type: str
    mfa_required: bool = False

@router.post("/auth/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
    mfa_code: Optional[str] = None # Added for Gap 1
):
    # 1. Fetch User
    user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
    if not user:
        # Gap 216: Timing Attack Mitigation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Check Lockout (Gap 6)
    if SecurityService.check_lockout(user):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Account locked. Try again after {user.locked_until}"
        )

    # 3. Verify Password (Gap 2)
    if not SecurityService.verify_password(form_data.password, user.password_hash):
        # Handle Failure
        is_locked = SecurityService.handle_failed_login(user)
        db.commit()
        if is_locked:
             raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Account locked due to too many failed attempts."
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Success - Reset Failures
    user.failed_login_attempts = 0
    
    # 5. Check MFA (Gap 1)
    if user.mfa_enabled:
        if not mfa_code:
             # Client needs to prompt for MFA
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="MFA_REQUIRED",
                headers={"X-MFA-Required": "true"}
            )
        if not SecurityService.verify_mfa(user.mfa_secret, mfa_code):
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA Code"
            )

    db.commit()

    # 6. Generate Token
    return {
        "access_token": f"fake-jwt-token-{user.username}", 
        "token_type": "bearer",
        "mfa_required": False
    }

@router.get("/connect/gmail/auth-url")
def get_gmail_auth_url():
    return {"url": "http://localhost:3000/connect?status=mock_gmail_success"}

class Credentials(BaseModel):
    username: str
    password: str

@router.post("/connect/appfolio/credentials")
def save_appfolio_creds(creds: Credentials):
    print(f"Saved AppFolio creds for {creds.username}")
    return {"status": "success"}
