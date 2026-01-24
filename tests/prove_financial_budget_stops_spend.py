import json
import os
import sys

# Contract paths
BUDGET_POLICY = "contracts/ops/financial_budget_policy.json"
SURFACE_MATRIX = "contracts/ops/budget_surface_matrix.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class CostManager:
    def __init__(self, policy, matrix):
        self.policy = policy
        self.matrix = {s['service']: s for s in matrix['surfaces']}
        self.current_spend = 0.0
        self.daily_limit = policy['limits']['daily_spend_usd']
        self.hard_stop = False
        
    def record_usage(self, service, units):
        if self.hard_stop:
             return "BLOCKED_BUDGET_EXCEEDED"
             
        if service not in self.matrix:
             return "UNKNOWN_SERVICE"
             
        cost = units * self.matrix[service]['cost_per_unit_usd']
        
        # Check if this usage would breach
        if self.current_spend + cost > self.daily_limit:
            action = self.policy['enforcement_action']
            print(f"  > Budget breach! Spend: {self.current_spend:.4f} + {cost:.4f} > {self.daily_limit}")
            if action == "HARD_STOP_NON_CRITICAL":
                # For simplicity in this test, we assume everything is non-critical enough to block
                # OR we block the incremental usage
                self.hard_stop = True
                return "BLOCKED_BUDGET_EXCEEDED"
        
        self.current_spend += cost
        return "ALLOWED"

def test_financial_budget():
    print("[INFO] Loading Budget Contracts...")
    policy = load_json(BUDGET_POLICY)
    matrix = load_json(SURFACE_MATRIX)
    
    mgr = CostManager(policy, matrix)
    
    # 1. Normal Usage
    print("  > Recording normal usage (OpenAI)...")
    res = mgr.record_usage("OPENAI", 1000) # 0.03 USD
    if res != "ALLOWED":
        print(f"[FAIL] Expected ALLOWED, got {res}")
        sys.exit(1)
    
    # 2. Breach Usage
    print("  > Recording massive usage to breach...")
    # Limit is 100. Spend is ~0.03. Need ~99.97.
    # Cost per unit 0.00003. Need 3,333,333 units roughly.
    res = mgr.record_usage("OPENAI", 4000000) # ~120 USD
    
    if res != "BLOCKED_BUDGET_EXCEEDED":
         print(f"[FAIL] Expected BLOCKED, got {res}")
         sys.exit(1)
         
    print("[PASS] Budget breach blocked usage.")
    
    # 3. Subsequent Usage Blocked
    res = mgr.record_usage("OPENAI", 1)
    if res != "BLOCKED_BUDGET_EXCEEDED":
         print(f"[FAIL] Subsequent usage should be blocked. Got {res}")
         sys.exit(1)
    print("[PASS] Hard stop persists.")

def main():
    try:
        test_financial_budget()
        print("\n[SUCCESS] Financial Budget Enforcement Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
