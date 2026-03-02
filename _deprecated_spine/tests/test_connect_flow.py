from fastapi.testclient import TestClient
from vte.main import app
import sys

client = TestClient(app)

def test_gmail_auth_url_generation():
    print("\n--- Testing Gmail Auth URL Generation ---")
    
    try:
        # 1. Call the Endpoint
        print(f"GET /api/v1/connect/gmail/auth-url")
        resp = client.get("/api/v1/connect/gmail/auth-url")
        
        if resp.status_code == 200:
            data = resp.json()
            url = data.get("url")
            print("SUCCESS: Received Auth URL")
            print(f"URL: {url[:50]}...")
            
            if "accounts.google.com" in url and "client_id" in url:
                print("VALIDATION: URL looks like a valid Google OAuth Link.")
                return True
            else:
                print("FAILURE: URL malformed.")
                return False
        else:
            print(f"FAILURE: Status {resp.status_code}")
            print(resp.text)
            
            if "credentials.json not found" in resp.text:
                print("HINT: Ensure credentials.json is in spine/")
            
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    if test_gmail_auth_url_generation():
        print("Connect Flow Verification Passed.")
        sys.exit(0)
    else:
        sys.exit(1)
