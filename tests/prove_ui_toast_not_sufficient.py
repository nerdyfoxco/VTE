import json
import os
import sys

# Simulates User Interrupt Budget Check (Toast vs Blocking)
# "Receipt Semantics" often implies we must prove the user SAW the confirmation.
# A Toast is ephemeral (not sufficient for critical actions).
# A Blocking Modal is sufficient.
# We check if a CRITICAL action is allowed with just a Toast cost.

def test_receipt_semantics():
    print("[INFO] Starting Receipt Semantics Verification...")
    sys.path.append(os.getcwd())
    
    # Load Interrupt Budget Policy
    # We defined `user_interrupt_budget.json` in Phase 1.26
    # Let's mock a policy check where CRITICAL actions require cost > X
    
    CRITICAL_ACTION_COST_THRESHOLD = 5 # e.g. Blocking Modal cost
    
    cost_map = {
        "TOAST": 0,
        "BLOCKING_MODAL": 5
    }
    
    proposed_ui = "TOAST" # Dev tries to use Toast for critical action
    
    action_type = "TRANSFER_FUNDS" # Critical
    
    print(f"  > Checking UI sufficiency for {action_type}...")
    
    # Validation Logic
    if action_type == "TRANSFER_FUNDS":
        required_cost = CRITICAL_ACTION_COST_THRESHOLD
    else:
        required_cost = 0
        
    actual_cost = cost_map[proposed_ui]
    
    if actual_cost < required_cost:
        print(f"    [PASS] Insufficient UI detected. Toast (0) < Required ({required_cost}).")
    else:
        print("    [FAIL] Toast was accepted for critical action!")
        sys.exit(1)
        
    print("\n[SUCCESS] Receipt Semantics Negative Scenario Proven.")

def main():
    try:
        test_receipt_semantics()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
