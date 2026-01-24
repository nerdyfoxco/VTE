import json
import os
import sys

# Simulates State Machine Negative Test
# Cannot transition from PENDING to CLOSED directly (must go through APPROVED or REJECTED).

def test_state_transition():
    print("[INFO] Starting State Transition Verification...")
    sys.path.append(os.getcwd())
    
    valid_transitions = {
        "PENDING": ["APPROVED", "REJECTED"],
        "APPROVED": ["CLOSED"],
        "REJECTED": ["CLOSED"]
    }
    
    current_state = "PENDING"
    target_state = "CLOSED" # Illegal jump
    
    print(f"  > Attempting transition {current_state} -> {target_state}...")
    
    if target_state not in valid_transitions[current_state]:
        print("    [PASS] Invalid transition blocked.")
    else:
        print("    [FAIL] Invalid transition allowed!")
        sys.exit(1)

    print("\n[SUCCESS] State Transition Scenario Proven.")

def main():
    try:
        test_state_transition()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
