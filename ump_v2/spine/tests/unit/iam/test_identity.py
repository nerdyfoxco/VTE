import pytest
import sys
import uuid
from pathlib import Path
from fastapi.testclient import TestClient

# Inject the src directory to import the API app
base_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(base_dir / "src"))

from main import app

client = TestClient(app)

def test_invalid_password_complexity():
    """
    Test 1: Ensures the system rejects passwords that do not meet VTE Tier 1 standards.
    """
    response = client.post("/auth/signup", json={
        "email": f"weak_{uuid.uuid4()}@vte.com",
        "password": "weak", # Fails the min_length=12 constraint
        "full_name": "Kevin Test",
        "tenant_id": "tnt_vte_1"
    })
    # Pydantic will throw a 422 Unprocessable Entity
    assert response.status_code == 422
    assert "password" in response.text.lower()

def test_duplicate_email_signup_rejection():
    """
    Test 2: Ensures the identity plane prevents account enumeration or hijacking.
    """
    unique_email = f"operator_{uuid.uuid4()}@vte.com"
    payload = {
        "email": unique_email,
        "password": "StrongPassword123!",
        "full_name": "Kevin Valid",
        "tenant_id": "tnt_vte_1"
    }
    
    # First Registration (Success)
    resp1 = client.post("/auth/signup", json=payload)
    assert resp1.status_code == 201
    assert resp1.json()["status"] == "CREATED"
    
    # Second Registration (Fail-Closed)
    resp2 = client.post("/auth/signup", json=payload)
    assert resp2.status_code == 400
    assert "already registered" in resp2.json()["detail"].lower()

def test_successful_signin_mfa_challenge():
    """
    Test 3: Corroborates that bypassing MFA to directly receive a token is impossible.
    """
    unique_email = f"operator_{uuid.uuid4()}@vte.com"
    valid_password = "StrongPassword123!"
    
    client.post("/auth/signup", json={
        "email": unique_email,
        "password": valid_password,
        "full_name": "MFA Kevin",
        "tenant_id": "tnt_vte_1"
    })
    
    # Attempt Sign In
    login_resp = client.post("/auth/signin", json={
        "email": unique_email,
        "password": valid_password
    })
    
    assert login_resp.status_code == 200
    data = login_resp.json()
    assert data["status"] == "MFA_REQUIRED"
    assert "mfa_token_id" in data
    assert data["challenge_type"] == "TOTP"

def test_failing_mfa_verification():
    """
    Test 4: Failing verification with an invalid/expired TOTP code.
    """
    verify_resp = client.post("/auth/mfa/verify", json={
        "mfa_token_id": "chl_faked_invalid_token",
        "totp_code": "000000" # Invalid code
    })
    
    assert verify_resp.status_code == 401
    assert "invalid" in verify_resp.json()["detail"].lower()
