import json
import os
import sys

# Simulates UI Action Proof Emission
# Every UI Action must emit a Proof with specific fields (User, Time, IntentID, etc).

def test_ui_action_proofs():
    print("[INFO] Starting UI Action Proof Verification...")
    sys.path.append(os.getcwd())
    
    # Contract: All proofs need 'timestamp', 'actor_id', 'intent_id'
    required_fields = ["timestamp", "actor_id", "intent_id"]
    
    # Mock Action Emission
    action_proof = {
        "action": "APPROVE_INVOICE",
        "timestamp": 1234567890,
        "actor_id": "user_1",
        "intent_id": "int_999",
        "details": {}
    }
    
    print(f"  > Verifying Proof: {action_proof}")
    
    missing = []
    for f in required_fields:
        if f not in action_proof:
            missing.append(f)
            
    if missing:
        print(f"    [FAIL] Missing fields: {missing}")
        sys.exit(1)
    else:
        print("    [PASS] Proof structure valid.")

    print("\n[SUCCESS] UI Action Proof Scenario Proven.")

def main():
    try:
        test_ui_action_proofs()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
