import json
import os
import sys

# Contract paths
BACKLOG_POLICY = "contracts/hitl/backlog_behavior_v1.json"
CAPACITY_MODEL = "contracts/hitl/hitl_capacity_model_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class BacklogMonitor:
    def __init__(self, policy):
        self.policy = policy
        self.circuit_breaker_open = False
        self.current_depth = 0
        
    def ingest_item(self):
        # Check circuit breaker
        if self.circuit_breaker_open:
            return "REJECTED_CIRCUIT_OPEN"
            
        self.current_depth += 1
        self._check_triggers()
        return "ACCEPTED"
        
    def _check_triggers(self):
        for trigger in self.policy['triggers']:
            if trigger['metric'] == "QUEUE_DEPTH":
                if self.current_depth > trigger['threshold']:
                    action = trigger['action']
                    print(f"  > Threshold {trigger['threshold']} breached (Depth: {self.current_depth}). Action: {action}")
                    if action == "ENABLE_INGEST_CIRCUIT_BREAKER":
                        self.circuit_breaker_open = True

def test_backlog_killswitch():
    print("[INFO] Loading Backlog Policy...")
    policy = load_json(BACKLOG_POLICY)
    monitor = BacklogMonitor(policy)
    
    # 1. Simulate Normal Ingest
    print("  > Simulating normal ingest...")
    # Fill up to threshold
    threshold = 0
    for t in policy['triggers']:
        if t['metric'] == "QUEUE_DEPTH":
            threshold = t['threshold']
            
    # Cheat: Set depth to threshold
    monitor.current_depth = threshold
    res = monitor.ingest_item() # threshold + 1
    
    if res != "ACCEPTED":
         print(f"[FAIL] Should have accepted item that caused breach (circuit opens AFTER). Got {res}")
         sys.exit(1)
         
    if not monitor.circuit_breaker_open:
         print("[FAIL] Circuit breaker should be OPEN after breach.")
         sys.exit(1)
         
    print("[PASS] Circuit breaker tripped on threshold breach.")
    
    # 2. Verify Rejection
    print("  > Attempting ingest with open circuit...")
    res = monitor.ingest_item()
    if res != "REJECTED_CIRCUIT_OPEN":
        print(f"[FAIL] Should have rejected item. Got {res}")
        sys.exit(1)
        
    print("[PASS] Ingest rejected when circuit is open.")

def main():
    try:
        test_backlog_killswitch()
        print("\n[SUCCESS] Backlog Kill Switch Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
