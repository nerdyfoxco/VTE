import json
import os
import sys
import time

# Contract paths
PRESENCE_POLICY = "contracts/hitl/hitl_presence_policy.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class PresenceManager:
    def __init__(self, policy):
        self.policy = policy
        self.agents = {} # {agent_id: {state, last_heartbeat}}
        
    def heartbeat(self, agent_id):
        self.agents[agent_id] = {
            "state": "AVAILABLE",
            "last_heartbeat": time.time()
        }
        
    def check_timeouts(self):
        now = time.time()
        missing_sec = self.policy['timeouts']['heartbeat_missing_sec']
        
        for agent_id, data in self.agents.items():
            if now - data['last_heartbeat'] > missing_sec:
                 if data['state'] != "OFFLINE":
                     print(f"  > Agent {agent_id} missed heartbeat (>{missing_sec}s). Marking OFFLINE.")
                     data['state'] = "OFFLINE"
            else:
                 # Logic for IDLE could go here, but focusing on heartbeat for this test
                 pass

    def get_status(self, agent_id):
        return self.agents.get(agent_id, {}).get("state", "UNKNOWN")

def test_presence_logic():
    print("[INFO] Loading Presence Policy...")
    policy = load_json(PRESENCE_POLICY)
    
    # Speed up timeout for test
    policy['timeouts']['heartbeat_missing_sec'] = 1 
    
    mgr = PresenceManager(policy)
    
    # 1. Heartbeat -> Available
    mgr.heartbeat("agent_1")
    if mgr.get_status("agent_1") != "AVAILABLE":
        print("[FAIL] Agent should be AVAILABLE after heartbeat.")
        sys.exit(1)
    print("[PASS] Heartbeat sets status to AVAILABLE.")
    
    # 2. Wait > timeout -> OFFLINE
    print("  > Waiting for timeout...")
    time.sleep(1.2)
    mgr.check_timeouts()
    
    if mgr.get_status("agent_1") != "OFFLINE":
         print(f"[FAIL] Agent should be OFFLINE. Got: {mgr.get_status('agent_1')}")
         sys.exit(1)
    print("[PASS] Missed heartbeat transitions to OFFLINE.")

def main():
    try:
        test_presence_logic()
        print("\n[SUCCESS] HITL Presence Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
