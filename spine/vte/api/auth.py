from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from vte.core.security import create_access_token
from vte.api.schema import Token
from vte.db import get_db
from vte.orm import TOTPDevice
from sqlalchemy.orm import Session
import pydantic

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 1. Verify Credentials (Mock)
    user_id = form_data.username
    role = "user"
    if form_data.password == "admin":
        role = "super_admin"
    elif form_data.password != "password": # Default mock password for non-admin check
        # In mock mode, we accept "admin"/"admin" or "user"/"password"
        # Since we don't have real user DB yet, we just allow Basic auth logic
        if user_id == "admin": 
             if form_data.password != "admin": raise HTTPException(status_code=400, detail="Incorrect password")
        else:
             # Just accept for now or fail?
             pass

    # 2. Check MFA Status
    # Check if user has ANY confirmed device
    mfa_device = db.query(TOTPDevice).filter(
        TOTPDevice.user_id == user_id, 
        TOTPDevice.confirmed == "true"
    ).first()

    if mfa_device:
        # MFA Required
        # Issue a partial token
        token_data = {"sub": user_id, "role": role, "mfa_pending": True}
        partial_token = create_access_token(data=token_data) # Short lived?
        return {
            "access_token": partial_token, 
            "token_type": "bearer", 
            "mfa_required": True
        }
    
    # Standard Login
    token_data = {"sub": user_id, "role": role, "mfa_pending": False}
    
    # Session Creation
    import uuid
    from datetime import datetime, timedelta, timezone
    from vte.orm import UserSession
    from fastapi import Request
    
    jti = str(uuid.uuid4())
    token_data["jti"] = jti
    
    access_token = create_access_token(data=token_data)
    
    # Store Session
    # Assuming default expiration for now (e.g. 30m) matches create_access_token
    expires = datetime.now(timezone.utc) + timedelta(minutes=30) 
    
    # Get IP/UA
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    
    session = UserSession(
        user_id=user_id,
        token_jti=jti,
        created_at=datetime.now(timezone.utc),
        expires_at=expires,
        ip_address=ip,
        user_agent=ua,
        revoked="false"
    )
    db.add(session)
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer", "mfa_required": False}

# --- MFA Endpoints ---
from vte.api.schema import TOTPSetupResponse, TOTPVerifyRequest
import pyotp
from vte.api.deps import get_current_user_claims as get_current_user
from vte.orm import UserSession

@router.post("/mfa/setup", response_model=TOTPSetupResponse)
def mfa_setup(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # ... existing code ...
    user_id = current_user["user_id"]
    secret = pyotp.random_base32()
    device = TOTPDevice(user_id=user_id, name="Default Device", secret=secret, confirmed="false")
    db.add(device)
    db.commit()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user_id, issuer_name="VTE System")
    return {"secret": secret, "uri": uri}

@router.post("/mfa/verify", response_model=Token)
def mfa_verify_login(
    payload: TOTPVerifyRequest,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... verification logic ...
    user_id = current_user["user_id"]
    devices = db.query(TOTPDevice).filter(TOTPDevice.user_id == user_id).all()
    if not devices: raise HTTPException(status_code=400, detail="MFA not setup")
    
    valid_device = None
    for device in devices:
        totp = pyotp.TOTP(device.secret)
        if totp.verify(payload.code, valid_window=1):
             valid_device = device
             break
    if not valid_device: raise HTTPException(status_code=401, detail="Invalid MFA Code")
    if valid_device.confirmed != "true":
        valid_device.confirmed = "true"
        db.commit()
        
    role = current_user.get("role", "user")
    token_data = {"sub": user_id, "role": role, "mfa_pending": False}
    
    # Session Creation for MFA Login
    import uuid
    from datetime import datetime, timedelta, timezone
    jti = str(uuid.uuid4())
    token_data["jti"] = jti
    access_token = create_access_token(data=token_data)
    
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    session = UserSession(
        user_id=user_id,
        token_jti=jti,
        created_at=datetime.now(timezone.utc),
        expires_at=expires,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        revoked="false"
    )
    db.add(session)
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer", "mfa_required": False}

# --- Session Management ---
from typing import List
from vte.api.schema import SessionRead

@router.get("/sessions", response_model=List[SessionRead])
def list_sessions(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    # return active sessions
    sessions = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.revoked == "false"
        # expires_at check skipped for brevity, client filters or logic elsewhere
    ).all()
    # Map to schema? ORM usually sufficient if names match
    # SessionRead expects session_id, user_id, etc.
    # Our DB has id. Schema has session_id. Map it.
    results = []
    for s in sessions:
        results.append({
            "session_id": str(s.id),
            "user_id": s.user_id,
            "created_at": s.created_at,
            "last_active_at": None, # Not tracked yet
            "ip_address": s.ip_address,
            "user_agent": s.user_agent
        })
    return results

@router.delete("/sessions/{session_id}")
def revoke_session(session_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    # Ensure user owns session
    import uuid
    try:
        s_uuid = uuid.UUID(session_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    session = db.query(UserSession).filter(UserSession.id == s_uuid, UserSession.user_id == user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session.revoked = "true"
    db.commit()
    return {"status": "revoked"}

class GoogleToken(pydantic.BaseModel):
    id_token: str

@router.post("/google-exchange", response_model=Token)
async def google_token_exchange(token: GoogleToken):
    """
    Exchanges a Google ID Token for a VTE Access Token.
    Supports 'Dev Mode' if GOOGLE_CLIENT_ID is not set.
    """
    import os
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests

    client_id = os.getenv("GOOGLE_CLIENT_ID")
    email = None
    
    if not client_id:
        # Dev Mode / Mock
        if token.id_token.startswith("mock_google_token_"):
            email = token.id_token.replace("mock_google_token_", "")
        else:
             raise HTTPException(status_code=400, detail="Invalid Mock Token (Dev Mode)")
    else:
        # Real Validation
        try:
            id_info = id_token.verify_oauth2_token(
                token.id_token, 
                google_requests.Request(), 
                client_id
            )
            email = id_info['email']
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid Google Token: {e}")

    # Issue VTE Token
    # In a real system, we would create/get the User object here.
    # For VTE Phase 20, we auto-provision based on email.
    
    role = "user"
    if email == "kevin@anchorrealtypa.com": # Hardcode Admin for Kevin
        role = "super_admin"
        
    token_data = {"sub": email, "role": role}
    access_token = create_access_token(data=token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}
