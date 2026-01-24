import json
import os
import sys

# Contract paths
LIFECYCLE_POLICY_PATH = "contracts/meta/contract_lifecycle_policy.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class LifecycleEnforcer:
    def __init__(self, policy):
        self.enforcement = policy['enforcement']
        
    def check_usage(self, contract_status, environment):
        if contract_status == "DRAFT":
            if environment == "PROD":
                return "BLOCKED"
        elif contract_status == "DEPRECATED":
            return "WARNING"
        elif contract_status == "RETIRED":
            return "BLOCKED"
            
        return "ALLOWED"

def test_lifecycle_enforcement():
    print("[INFO] Loading Lifecycle Policy...")
    policy = load_json(LIFECYCLE_POLICY_PATH)
    enforcer = LifecycleEnforcer(policy)
    
    # 1. Test DRAFT
    print("[INFO] Testing DRAFT status...")
    if enforcer.check_usage("DRAFT", "DEV") != "ALLOWED":
        print("[FAIL] Draft blocked in DEV!")
        sys.exit(1)
    if enforcer.check_usage("DRAFT", "PROD") != "BLOCKED":
        print("[FAIL] Draft allowed in PROD!")
        sys.exit(1)
    print("[PASS] Draft status enforced.")
    
    # 2. Test DEPRECATED
    print("[INFO] Testing DEPRECATED status...")
    if enforcer.check_usage("DEPRECATED", "PROD") != "WARNING":
        print("[FAIL] Deprecated did not warn!")
        sys.exit(1)
    print("[PASS] Deprecated status warns.")

    # 3. Test RETIRED
    print("[INFO] Testing RETIRED status...")
    if enforcer.check_usage("RETIRED", "PROD") != "BLOCKED":
        print("[FAIL] Retired allowed!")
        sys.exit(1)
    print("[PASS] Retired status blocked.")

def main():
    try:
        test_lifecycle_enforcement()
        print("\n[SUCCESS] Contract Lifecycle Enforcement Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
