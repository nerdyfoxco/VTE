import json
import os
import sys

# Contract paths
ACCOUNT_LIFECYCLE_PATH = "contracts/iam/account_lifecycle_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class SessionManager:
    def __init__(self, lifecycle_policy):
        self.transitions = lifecycle_policy['transitions']
        self.active_sessions = {"user_1": ["sess_A", "sess_B"]}
        self.account_status = {"user_1": "ACTIVE"}

    def change_status(self, user_id, new_status):
        current_status = self.account_status.get(user_id, "UNKNOWN")
        transition_key = f"{current_status}_TO_{new_status}"
        
        # Check transition logic
        if transition_key in self.transitions:
            config = self.transitions[transition_key]
            side_effects = config['side_effects']
            
            if "DISCONNECT_ACTIVE_SESSIONS" in side_effects:
                print(f"  > Executing Side Effect: DISCONNECT_ACTIVE_SESSIONS for {user_id}")
                if user_id in self.active_sessions:
                    del self.active_sessions[user_id]
            
        self.account_status[user_id] = new_status

def test_account_disable():
    print("[INFO] Loading Policy...")
    policy = load_json(ACCOUNT_LIFECYCLE_PATH)
    manager = SessionManager(policy)
    
    user = "user_1"
    
    # 1. Verify Active Sessions exist
    if user not in manager.active_sessions:
        print("[FAIL] Setup error, no active sessions.")
        sys.exit(1)
    print(f"[INFO] User {user} has active sessions: {manager.active_sessions[user]}")
    
    # 2. Disable Account
    print(f"[INFO] Disabling Account {user}...")
    manager.change_status(user, "DISABLED")
    
    # 3. Verify Revocation
    if user in manager.active_sessions:
        print(f"[FAIL] Sessions still active after disable! {manager.active_sessions[user]}")
        sys.exit(1)
        
    print("[PASS] Account Disable revoked all sessions immediately.")

def main():
    try:
        test_account_disable()
        print("\n[SUCCESS] Account Lifecycle Safety Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
