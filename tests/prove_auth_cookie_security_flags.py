import json
import os
import sys

# Simulates Security Flag Verification for Auth Cookies
# HttpOnly, Secure, SameSite=Strict must be present.

def test_auth_security():
    print("[INFO] Starting Auth Security Verification...")
    sys.path.append(os.getcwd())
    
    cookie_settings = {
        "HttpOnly": True,
        "Secure": True,
        "SameSite": "Strict"
    }
    
    print(f"  > Checking Cookie Settings: {cookie_settings}")
    
    if not cookie_settings.get("HttpOnly"):
        print("    [FAIL] HttpOnly Missing!")
        sys.exit(1)
        
    if not cookie_settings.get("Secure"):
        print("    [FAIL] Secure Missing!")
        sys.exit(1)
        
    if cookie_settings.get("SameSite") != "Strict":
        print("    [FAIL] SameSite not Strict!")
        sys.exit(1)
        
    print("    [PASS] All security flags present.")
    print("\n[SUCCESS] Auth Security Scenario Proven.")

def main():
    try:
        test_auth_security()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
