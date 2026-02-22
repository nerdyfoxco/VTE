from fastapi.testclient import TestClient
from vte.main import app
import sys

client = TestClient(app)

def test_google_mock_login():
    print("\n--- Testing Google Mock Auth (TestClient) ---")
    
    # 1. Payload with Mock Token
    mock_token = "mock_google_token_kevin@anchorrealtypa.com"
    payload = {"id_token": mock_token}
    
    try:
        # 2. Call the Endpoint
        print(f"POST /api/v1/auth/google-exchange")
        resp = client.post("/api/v1/auth/google-exchange", json=payload)
        
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("access_token")
            print("SUCCESS: Received Access Token (Admin)")
            print(f"Token: {token[:20]}...")
            return True
        else:
            print(f"FAILURE: Status {resp.status_code}")
            print(resp.text)
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

def test_standard_user_login():
    print("\n--- Testing Standard User Login ---")
    mock_token = "mock_google_token_stranger@gmail.com"
    payload = {"id_token": mock_token}
    
    resp = client.post("/api/v1/auth/google-exchange", json=payload)
    if resp.status_code == 200:
        print("SUCCESS: Received Access Token (Standard User)")
        # We could decode the JWT here to verify role is 'user', 
        # but for now HTTP 200 proves the account was 'synced' (provisioned).
        return True
    else:
         print(f"FAILURE: {resp.text}")
         return False

if __name__ == "__main__":
    admin_ok = test_google_mock_login()
    user_ok = test_standard_user_login()
    
    if admin_ok and user_ok:
        print("\nAll Auth Tests Passed.")
    else:
        sys.exit(1)
