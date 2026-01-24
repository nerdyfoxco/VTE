import json
import os
import sys

class ActionController:
    def __init__(self):
        self.sensitive_actions = {"DELETE_ACCOUNT", "TRANSFER_FUNDS", "CHANGE_PASSWORD"}
        
    def perform_action(self, action_name, session_assurance_level):
        print(f"  > Requesting {action_name} with Assurance Level {session_assurance_level}")
        
        if action_name in self.sensitive_actions:
            if session_assurance_level < 2:
                print("    [BLOCK] Step-Up Auth Required")
                return "STEP_UP_REQUIRED"
                
        return "SUCCESS"

def test_step_up_enforcement():
    print("[INFO] Testing Step-Up Enforcement...")
    controller = ActionController()
    
    # 1. Test Sensitive Action with Low Assurance
    res = controller.perform_action("DELETE_ACCOUNT", session_assurance_level=1)
    if res != "STEP_UP_REQUIRED":
        print(f"[FAIL] Sensitive action allowed without step-up! Result: {res}")
        sys.exit(1)
    print("[PASS] Sensitive action blocked correctly.")
    
    # 2. Test Sensitive Action with High Assurance
    res = controller.perform_action("DELETE_ACCOUNT", session_assurance_level=2)
    if res != "SUCCESS":
         print(f"[FAIL] High assurance blocked valid action! Result: {res}")
         sys.exit(1)
    print("[PASS] High assurance allowed action.")

def main():
    try:
        test_step_up_enforcement()
        print("\n[SUCCESS] Step-Up Enforcement Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
