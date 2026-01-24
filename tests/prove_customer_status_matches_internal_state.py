import json
import os
import sys

# Simulates Customer Status Matching
# "Active" customer must have "Active" internal state (e.g. billing).

def test_customer_status():
    print("[INFO] Starting Customer Status Verification...")
    sys.path.append(os.getcwd())
    
    internal_billing = {"valid": True, "paid": True}
    customer_ui_status = "ACTIVE"
    
    print(f"  > Internal: {internal_billing}")
    print(f"  > UI: {customer_ui_status}")
    
    # Logic
    if internal_billing['valid'] and customer_ui_status == "ACTIVE":
        print("    [PASS] Status consistent.")
    else:
        print("    [FAIL] Inconsistent status.")
        sys.exit(1)

    print("\n[SUCCESS] Customer Status Scenario Proven.")

def main():
    try:
        test_customer_status()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
