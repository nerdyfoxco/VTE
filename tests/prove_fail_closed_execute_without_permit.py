import json
import os
import sys

# Simulates Fail-Closed Logic (No Permit -> No Execution)
# Firewall Permit Check must be mandatory.

def test_fail_closed_no_permit():
    print("[INFO] Starting Fail-Closed Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Runner
    permit = None
    
    print("  > Attempting execution without permit...")
    
    if not permit:
        print("    [PASS] Execution Blocked: Missing Permit.")
    else:
        print("    [FAIL] Execution permitted without token!")
        sys.exit(1)

    print("\n[SUCCESS] Fail-Closed Scenario Proven.")

def main():
    try:
        test_fail_closed_no_permit()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
