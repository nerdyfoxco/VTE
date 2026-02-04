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
            print("SUCCESS: Received Access Token")
            print(f"Token: {token[:20]}...")
            return True
        else:
            print(f"FAILURE: Status {resp.status_code}")
            print(resp.text)
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if test_google_mock_login():
        print("Google Auth Verification Passed.")
    else:
        sys.exit(1)
