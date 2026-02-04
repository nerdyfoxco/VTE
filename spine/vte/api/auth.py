from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from vte.core.security import create_access_token
from vte.api.schema import Token

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Mock Auth Logic:
    # In production, check DB for user + hashed password.
    # For VTE MVP/Phase 11: Accept any user, assign role 'admin' if password is 'admin'.
    
    user_id = form_data.username
    role = "user"
    if form_data.password == "admin":
        role = "super_admin"
    
    token_data = {"sub": user_id, "role": role}
    access_token = create_access_token(data=token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

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
