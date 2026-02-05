from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
import json
from google_auth_oauthlib.flow import Flow

router = APIRouter()

# Constants
CREDENTIALS_FILE = "client_secret.json" # Switched from credentials.json due to FS lock
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
REDIRECT_URI = "http://localhost:3000/connect/callback" # Assumed standard for Next.js

class CallbackRequest(BaseModel):
    code: str

@router.get("/gmail/auth-url")
def get_gmail_auth_url():
    """
    Generates the Google OAuth2 Authorization URL.
    """
    if not os.path.exists(CREDENTIALS_FILE):
        raise HTTPException(status_code=500, detail="App credentials.json not found in server root.")

    try:
        # Create Flow
        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        # Generate URL
        auth_url, _ = flow.authorization_url(prompt='consent')
        
        return {"url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Auth URL: {str(e)}")

@router.post("/gmail/callback")
def gmail_callback(request: CallbackRequest):
    """
    Exchanges the Auth Code for User Credentials (Tokens).
    """
    if not os.path.exists(CREDENTIALS_FILE):
         raise HTTPException(status_code=500, detail="App credentials.json not found.")

    try:
        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        # Exchange Code
        flow.fetch_token(code=request.code)
        
        # Get Credentials
        creds = flow.credentials
        
        # SAVE Credentials (Per User)
        # In a real SaaS, we store this in the DB encrypted, linked to the User ID.
        # For VTE Phase 20 (Single Tenant / Admin), we'll save it as 'token.json' 
        # which is what GmailClient looks for.
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
        return {"status": "success", "message": "Gmail Connected Successfully"}
        
    except Exception as e:
        # Log the full error for debugging
        print(f"OAuth Exchange Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

class AppFolioCreds(BaseModel):
    username: str
    password: str

@router.post("/appfolio/credentials")
def save_appfolio_creds(creds: AppFolioCreds):
    """
    Saves AppFolio credentials to local storage (MVP).
    WARNING: Not encrypted. For Phase 2 Demo only.
    """
    try:
        data = {
            "username": creds.username,
            "password": creds.password
        }
        with open("appfolio_creds.json", "w") as f:
            json.dump(data, f)
            
        return {"status": "success", "message": "AppFolio Credentials Saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
