import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_sessions():
    print("1. Login...")
    # Using Basic Login (MFA valid window=1 allows simple flow if lucky, or we use Setup flow)
    # But for simplicity, let's just use /auth/token basic if admin uses it?
    # Wait, MFA enforced if enabled? Admin has NO MFA enabled by default?
    # I cleared DB? No, I ran verifying_mfa.py which SETUP MFA for admin.
    # So Admin now requires MFA!
    # I need to use MFA flow to get a token.
    # Or creating a NEW user 'test_user' via seed?
    # verify_mfa.py left Admin in state where MFA is required.
    
    # I'll try basic login. If mfa_required, I fail context.
    # Actually, I can use the SECRET I know from verify_mfa output if likely?
    # No, secret is random.
    # I should use a new user or reset DB.
    # Or better: `verify_sessions.py` should setup MFA if needed or handle it.
    
    # Let's try to login as 'admin'.
    r = requests.post(f"{BASE_URL}/auth/token", data={"username": "admin", "password": "admin"})
    data = r.json()
    
    if data.get("mfa_required"):
        print("MFA Required for Admin. Cannot proceed easily without knowing secret.")
        print("Resetting DB or handling MFA is needed.")
        sys.exit(1)
        
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Logged in. Value:", token[:10] + "...")
    
    print("2. List Sessions...")
    r = requests.get(f"{BASE_URL}/auth/sessions", headers=headers)
    if r.status_code != 200:
        print(f"FAILED list sessions: {r.text}")
        sys.exit(1)
        
    sessions = r.json()
    print(f"   Found {len(sessions)} sessions.")
    if len(sessions) == 0:
        print("FAILURE: No session found for current user.")
        sys.exit(1)
        
    my_session = sessions[0]
    sid = my_session["session_id"]
    print(f"   Target Session: {sid}")
    
    print("3. Revoke Session...")
    r = requests.delete(f"{BASE_URL}/auth/sessions/{sid}", headers=headers)
    if r.status_code != 200:
        print(f"FAILED revoke: {r.text}")
        sys.exit(1)
    
    print("   Revoked.")
    
    print("4. Verify Token is Rejected...")
    r = requests.get(f"{BASE_URL}/auth/sessions", headers=headers)
    if r.status_code == 401:
        print("SUCCESS: Token rejected (401).")
    else:
        print(f"FAILURE: Token still accepted! Status: {r.status_code}")
        print(r.text)
        sys.exit(1)

if __name__ == "__main__":
    test_sessions()
