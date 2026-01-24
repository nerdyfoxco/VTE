import json
import os
import sys
import datetime

# Contract paths
RETENTION_POLICY_PATH = "contracts/privacy/retention_policy_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class RetentionEnforcer:
    def __init__(self, policy):
        self.schedules = policy['schedules']

    def check_retention(self, data_type, age_days):
        if data_type not in self.schedules:
            return "UNKNOWN_TYPE"
            
        schedule = self.schedules[data_type]
        limit = schedule['retention_days']
        action = schedule['post_action']
        
        if age_days > limit:
            return action
        return "KEEP"

def test_retention_logic():
    print("[INFO] Loading Retention Policy...")
    policy = load_json(RETENTION_POLICY_PATH)
    enforcer = RetentionEnforcer(policy)
    
    # 1. Test Raw Evidence (90 days)
    print("[INFO] Testing 'raw_evidence_artifacts' (Limit: 90 days)...")
    if enforcer.check_retention("raw_evidence_artifacts", 89) != "KEEP":
        print("[FAIL] Deleted raw evidence too early!")
        sys.exit(1)
        
    if enforcer.check_retention("raw_evidence_artifacts", 91) != "HARD_DELETE":
        print("[FAIL] Failed to HARD_DELETE raw evidence after expiry!")
        sys.exit(1)
        
    print("[PASS] Raw evidence retention enforced.")

    # 2. Test Audit Logs (7 Years = 2555 days)
    print("[INFO] Testing 'audit_logs' (Limit: 2555 days)...")
    if enforcer.check_retention("audit_logs", 2000) != "KEEP":
         print("[FAIL] Archived audit logs too early!")
         sys.exit(1)

    if enforcer.check_retention("audit_logs", 2600) != "ARCHIVE_COLD_STORAGE":
         print("[FAIL] Failed to ARCHIVE audit logs after expiry!")
         sys.exit(1)

    print("[PASS] Audit log retention enforced.")

def main():
    try:
        test_retention_logic()
        print("\n[SUCCESS] Retention Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
