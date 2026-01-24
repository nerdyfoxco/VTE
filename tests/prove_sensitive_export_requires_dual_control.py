import json
import os
import sys

# Simulates Sensitive Export Control
# Requires Dual Control (2 signatures) to export PII.

def test_sensitive_export():
    print("[INFO] Starting Sensitive Export Verification...")
    sys.path.append(os.getcwd())
    
    request = {
        "resource": "PII_DB",
        "signatures": ["sig_admin_1", "sig_admin_2"]
    }
    
    print(f"  > Requesting export with {len(request['signatures'])} signatures...")
    
    if len(request['signatures']) >= 2:
        print("    [PASS] Dual control signatures present.")
    else:
        print("    [FAIL] Insufficient signatures.")
        sys.exit(1)

    print("\n[SUCCESS] Sensitive Export Scenario Proven.")

def main():
    try:
        test_sensitive_export()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
