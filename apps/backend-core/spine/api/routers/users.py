from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from spine.db.engine import get_db
from spine.db.models import DBUser
from spine.core.security import SecurityService
from spine.ops.audit import AuditLogger
import secrets

router = APIRouter()

class UserInvite(BaseModel):
    email: EmailStr
    role: str = "user"

class PasswordResetRequest(BaseModel):
    username: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

# Gap 12: Invite User
@router.post("/users/invite", status_code=status.HTTP_201_CREATED)
def invite_user(
    invite: UserInvite, 
    db: Session = Depends(get_db),
    # In real world: current_user: DBUser = Depends(get_current_active_user)
):
    # Check if exists
    if db.query(DBUser).filter(DBUser.username == invite.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    token = secrets.token_urlsafe(32)
    user = DBUser(
        username=invite.email, # Username is email
        role=invite.role,
        tenant_id="system", # Default for now
        invitation_token=token,
        invitation_expires_at=datetime.utcnow() + timedelta(days=7),
        email_verified=False
    )
    db.add(user)
    db.commit()
    
    AuditLogger.log(db, "admin", "USER_INVITED", f"email:{invite.email}")

    # Mock Email Send
    print(f"EMAIL TO {invite.email}: Join VTE at /invite?token={token}")
    return {"message": "Invitation sent"}

# Gap 11: Forgot Password
@router.post("/auth/forgot-password")
def forgot_password(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    user = db.query(DBUser).filter(DBUser.username == request.username).first()
    if not user:
        AuditLogger.log(db, "anonymous", "RESET_REQUEST_UNKNOWN", f"target:{request.username}")
        # Return 200 to prevent Enum attacks
        return {"message": "If user exists, email sent."}
    
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=15)
    db.commit()
    
    AuditLogger.log(db, "anonymous", "RESET_REQUEST_INITIATED", f"target:{user.username}")

    # Mock Email
    print(f"EMAIL TO {user.username}: Reset at /reset?token={token}")
    return {"message": "If user exists, email sent."}

# Gap 11: Reset Confirm
@router.post("/auth/reset-password")
def reset_password_confirm(
    confirm: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    user = db.query(DBUser).filter(DBUser.reset_token == confirm.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
        
    if user.reset_token_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")
        
    # Complexity Check
    SecurityService.check_password_complexity(confirm.new_password)
    
    user.password_hash = SecurityService.get_password_hash(confirm.new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    user.password_changed_at = datetime.utcnow()
    # Unlock if locked
    user.locked_until = None 
    user.failed_login_attempts = 0
    
    db.commit()
    AuditLogger.log(db, user.username, "PASSWORD_RESET_SUCCESS", "self_service")
    return {"message": "Password updated successfully"}
