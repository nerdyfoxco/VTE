import json
import os
import sys

# Contract paths
ESCALATION_POLICY = "contracts/ux/escalation_policy_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class EscalationEngine:
    def __init__(self, policy):
        self.levels = sorted(policy['levels'], key=lambda x: x['level'])
        
    def check_sla(self, time_elapsed_percent, breached=False):
        print(f"  > Checking status: {time_elapsed_percent}% elapsed, Breached={breached}")
        actions = []
        
        # Simple logic mapping to policy triggers
        if breached:
             # Level 2 match
             for l in self.levels:
                 if "SLA_BREACHED" in l['trigger'] and "+ 1h" not in l['trigger']:
                     actions.append(l['action'])
                     
        elif time_elapsed_percent > 80:
             # Level 1 match
             for l in self.levels:
                 if "SLA_WARNING" in l['trigger']:
                     actions.append(l['action'])
                     
        return actions

def test_escalation_triggers():
    print("[INFO] Loading Escalation Policy...")
    policy = load_json(ESCALATION_POLICY)
    engine = EscalationEngine(policy)
    
    # 1. Test Warning
    actions = engine.check_sla(85, breached=False)
    if "NOTIFY_ASSIGNEE_URGENT" not in actions:
        print(f"[FAIL] Warning trigger failed! Got: {actions}")
        sys.exit(1)
    print("[PASS] SLA Warning triggers Urgent Notification.")
    
    # 2. Test Breach
    actions = engine.check_sla(105, breached=True)
    if "REASSIGN_TO_MANAGER_POOL" not in actions:
         print(f"[FAIL] Breach trigger failed! Got: {actions}")
         sys.exit(1)
    print("[PASS] SLA Breach triggers Reassignment.")

def main():
    try:
        test_escalation_triggers()
        print("\n[SUCCESS] Escalation Trigger Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
