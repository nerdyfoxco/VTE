from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class OIDCConfiguration(BaseModel):
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    token_endpoint_auth_methods_supported: List[str]
    response_types_supported: List[str]
    subject_types_supported: List[str]
    id_token_signing_alg_values_supported: List[str]
    scopes_supported: List[str]
    claims_supported: List[str]

@router.get("/openid-configuration", response_model=OIDCConfiguration)
def get_oidc_configuration():
    """
    Returns the OpenID Connect discovery metadata.
    """
    # In a real deployed environment, 'issuer' should be dynamic or env-configured.
    # For VTE Localhost Proof:
    issuer_url = "http://localhost:8000"
    
    return {
        "issuer": issuer_url,
        "authorization_endpoint": f"{issuer_url}/api/v1/auth/login", # Standard UI login
        "token_endpoint": f"{issuer_url}/api/v1/auth/token",
        "token_endpoint_auth_methods_supported": ["client_secret_post"],
        "response_types_supported": ["token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["HS256"],
        "scopes_supported": ["openid", "profile", "email"],
        "claims_supported": ["sub", "iss", "aud", "exp", "iat", "email", "role"]
    }
