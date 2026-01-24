import json
import os
import sys

# Contract paths
BUDGET_POLICY_PATH = "contracts/meta/change_budget_policy_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def check_budget(change_type):
    policy = load_json(BUDGET_POLICY_PATH)
    budgets = policy['budgets']
    
    if change_type not in budgets:
        # If not tracked, assume allowed (or maybe strict deny?)
        # Let's say we only track specific high risk things.
        return "ALLOWED"
        
    budget = budgets[change_type]
    limit = budget['limit']
    usage = budget['current_usage']
    
    if usage >= limit:
        return "BLOCKED_BUDGET_EXCEEDED"
        
    return "ALLOWED"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_change_budget.py <CHANGE_TYPE>")
        sys.exit(1)
        
    res = check_budget(sys.argv[1])
    print(res)
    if "BLOCKED" in res:
        sys.exit(1)
