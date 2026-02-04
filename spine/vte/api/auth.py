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
