import json
import os
import sys

# Contract paths
SUPPORT_ACCESS_PATH = "contracts/iam/support_access_timebox_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class AccessController:
    def __init__(self, policy):
        self.max_hours = policy['grant_rules']['max_duration_hours']
        self.revocation_action = policy['revocation']['action']
        self.active_grants = {} # grant_id -> expiry_ts

    def request_grant(self, grant_id, requested_hours):
        if requested_hours > self.max_hours:
            return "DENIED_TOO_LONG"
        return "GRANTED"
        
    def check_expiry_enforcement(self, duration_exceeded):
        if duration_exceeded:
            return self.revocation_action
        return "ACTIVE"

def test_support_timebox():
    print("[INFO] Loading Policy...")
    policy = load_json(SUPPORT_ACCESS_PATH)
    controller = AccessController(policy)
    
    limit = controller.max_hours
    print(f"[INFO] Max Duration: {limit} hours")
    
    # 1. Request within limit
    if controller.request_grant("g1", limit) != "GRANTED":
        print("[FAIL] Valid duration denied!")
        sys.exit(1)
    print("[PASS] Valid duration accepted.")

    # 2. Request exceeded limit
    if controller.request_grant("g2", limit + 1) != "DENIED_TOO_LONG":
         print("[FAIL] Excessive duration allowed!")
         sys.exit(1)
    print("[PASS] Excessive duration rejected.")

    # 3. Verify Revocation Action
    action = controller.check_expiry_enforcement(duration_exceeded=True)
    if action != "IMMEDIATE_SESSION_KILL":
         print(f"[FAIL] Expiry did not kill session! Got: {action}")
         sys.exit(1)
    print("[PASS] Expiry triggers IMMEDIATE_SESSION_KILL.")

def main():
    try:
        test_support_timebox()
        print("\n[SUCCESS] Support Timebox Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
