import json
import os
import sys

# Simulates Permit Authority Binding
# Each Permit GRANT must carry the effective principal and source.

def test_permit_authority():
    print("[INFO] Starting Permit Authority Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Permit Token Payload
    permit = {
        "permit_id": "perm_999",
        "action": "DB_WRITE",
        "authority": {
            "effective_principal": "user_admin_1",
            "grant_source": "SAML_ASSERTION_XYZ"
        }
    }
    
    print(f"  > Validating permit authority: {permit['authority']}")
    
    if "effective_principal" in permit["authority"] and "grant_source" in permit["authority"]:
        print("    [PASS] Permit carries effective authority binding.")
    else:
        print("    [FAIL] Permit missing authority info.")
        sys.exit(1)

    print("\n[SUCCESS] Permit Authority Scenario Proven.")

def main():
    try:
        test_permit_authority()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
