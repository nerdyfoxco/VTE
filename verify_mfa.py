import requests
import pyotp
import sys
import time

BASE_URL = "http://localhost:8000/api/v1"

def get_initial_token(username="admin", password="admin"):
    payload = {"username": username, "password": password}
    r = requests.post(f"{BASE_URL}/auth/token", data=payload)
    if r.status_code != 200:
        print(f"FAILED initial login: {r.text}")
        sys.exit(1)
    return r.json()

def test_mfa_flow():
    print("1. Initial Login (No MFA)...")
    token_resp = get_initial_token()
    token = token_resp["access_token"]
    
    if token_resp.get("mfa_required"):
        print("WARNING: MFA already required? Did test run before?")
        # Iterate to next steps?
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("2. Setup MFA...")
    r = requests.post(f"{BASE_URL}/auth/mfa/setup", headers=headers)
    if r.status_code != 200:
        print(f"FAILED setup: {r.text}")
        sys.exit(1)
    
    setup_data = r.json()
    secret = setup_data["secret"]
    print(f"   Secret: {secret}")
    
    # 3. Verify MFA Setup (Confirm Device)
    print("3. Verify MFA Setup...")
    totp = pyotp.TOTP(secret)
    code = totp.now()
    
    r = requests.post(
        f"{BASE_URL}/auth/mfa/verify", 
        headers=headers,
        json={"code": code}
    )
    if r.status_code != 200:
        print(f"FAILED verification: {r.text}")
        sys.exit(1)
        
    full_token = r.json()["access_token"]
    print("   Device Confirmed. Full Token received.")
    
    # 4. Enforce MFA on Re-Login
    print("4. Testing MFA Enforcement on basic Login...")
    token_resp_2 = get_initial_token()
    
    if not token_resp_2.get("mfa_required"):
        print("FAILURE: Login did not require MFA after setup.")
        sys.exit(1)
        
    partial_token = token_resp_2["access_token"]
    print("   Received Partial Token + mfa_required=True")
    
    # 5. Complete Login with Partial Token
    print("5. Completing Login...")
    
    # Wait for next TOTP code window just in case
    time.sleep(1) 
    code_2 = totp.now()
    
    r = requests.post(
        f"{BASE_URL}/auth/mfa/verify", 
        headers={"Authorization": f"Bearer {partial_token}"},
        json={"code": code_2}
    )
    
    if r.status_code != 200:
        print(f"FAILED final login: {r.text}")
        sys.exit(1)
        
    final_token = r.json()
    if final_token.get("mfa_required"):
         print("FAILURE: Final response still says MFA required.")
         sys.exit(1)
         
    print("SUCCESS: End-to-End MFA Flow Verified.")

if __name__ == "__main__":
    test_mfa_flow()
