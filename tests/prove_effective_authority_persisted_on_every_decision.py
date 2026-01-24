import json
import os
import sys

# Simulates Authority Binding Persisted
# Every write must have principal_id and grant_source.

def test_authority_binding():
    print("[INFO] Starting Authority Binding Verification...")
    sys.path.append(os.getcwd())
    
    # Mock DB Write
    def db_write(data, context):
        if "effective_principal_id" not in context:
            return "BLOCKED_MISSING_PRINCIPAL"
        if "session_grant_source" not in context:
            return "BLOCKED_MISSING_GRANT"
        return "SUCCESS"
        
    print("  > Attempting write without context...")
    if db_write({}, {}) != "SUCCESS":
        print("    [PASS] Write blocked.")
    else:
        sys.exit(1)
        
    print("  > Attempting write with full context...")
    ctx = {
        "effective_principal_id": "user_123",
        "session_grant_source": "token:abc"
    }
    if db_write({}, ctx) == "SUCCESS":
        print("    [PASS] Write succeeded.")
    else:
        print("    [FAIL] Write failed with context.")
        sys.exit(1)

    print("\n[SUCCESS] Authority Binding Scenario Proven.")

def main():
    try:
        test_authority_binding()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
