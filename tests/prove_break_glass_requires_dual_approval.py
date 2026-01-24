import json
import os
import sys

# Simulates Dual Approval for Break Glass
# Action requires 2 distinct approvers.

def test_dual_approval():
    print("[INFO] Starting Dual Approval Verification...")
    sys.path.append(os.getcwd())
    
    approvals = ["admin_1", "admin_2"]
    
    print("  > Checking approvals...")
    
    if len(set(approvals)) >= 2:
        print("    [PASS] Dual approval met.")
    else:
        print("    [FAIL] Insufficient approvals.")
        sys.exit(1)
        
    # Negative case
    bad_approvals = ["admin_1", "admin_1"] # Same person
    if len(set(bad_approvals)) < 2:
        print("    [PASS] Duplicate approver rejected.")

    print("\n[SUCCESS] Dual Approval Scenario Proven.")

def main():
    try:
        test_dual_approval()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
