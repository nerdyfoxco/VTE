import json
import os
import sys

# Contract paths
ABSTENTION_POLICY = "contracts/ai/abstention_policy_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class AI_Router:
    def __init__(self, policy):
        self.policy = policy
        
    def route(self, prediction_confidence):
        thresholds = self.policy['thresholds']
        
        if prediction_confidence >= thresholds['auto_approve_min_confidence']:
            return "AUTO_APPROVE"
        elif prediction_confidence <= thresholds['abstain_max_confidence']:
            return self.policy['action_on_abstain']
        else:
            # Grey zone - debatable, but let's say "FLAG_FOR_AUDIT" or similar
            # For this policy, let's assume anything between 0.85 and 0.95 is also HITL or AUDIT
            # But strictly following the "abstain_max", if it's 0.90, it's > abstains (0.85) and < auto (0.95)
            # The policy is slightly ambiguous in the gap. Let's assume GAP = HITL for safety.
            return "ROUTE_TO_HITL"

def test_abstention_logic():
    print("[INFO] Loading Abstention Policy...")
    policy = load_json(ABSTENTION_POLICY)
    router = AI_Router(policy)
    
    # 1. High Confidence -> Auto Approve
    conf = 0.98
    res = router.route(conf)
    if res != "AUTO_APPROVE":
        print(f"[FAIL] Expected AUTO_APPROVE for {conf}, got {res}")
        sys.exit(1)
    print(f"[PASS] Confidence {conf} -> AUTO_APPROVE")
    
    # 2. Low Confidence -> Abstain/HITL
    conf = 0.60
    res = router.route(conf)
    if res != "ROUTE_TO_HITL":
        print(f"[FAIL] Expected ROUTE_TO_HITL for {conf}, got {res}")
        sys.exit(1)
    print(f"[PASS] Confidence {conf} -> ROUTE_TO_HITL (Abstained)")
    
    # 3. Boundary
    conf = 0.85
    res = router.route(conf)
    if res != "ROUTE_TO_HITL":
         print(f"[FAIL] Expected ROUTE_TO_HITL for {conf}, got {res}")
         sys.exit(1)
    print(f"[PASS] Confidence {conf} -> ROUTE_TO_HITL (Abstained)")

def main():
    try:
        test_abstention_logic()
        print("\n[SUCCESS] Abstention Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
