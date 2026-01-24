import json
import os
import sys

# Contract paths
COMPOSITION_RULES = "contracts/iam/role_composition_rules_v1.json"
ROLE_MATRIX = "contracts/iam/role_capability_matrix.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def test_multi_role_composition():
    print("[INFO] Loading Role Definitions...")
    rules = load_json(COMPOSITION_RULES)
    matrix = load_json(ROLE_MATRIX)
    
    roles = matrix['roles']
    strategy = rules['composition_strategy']
    
    if strategy != "UNION":
        print(f"[FAIL] Only UNION strategy is supported in this canary. Got: {strategy}")
        sys.exit(1)
        
    # Simulate User with AGENT and AUDITOR roles
    user_roles = ["AGENT", "AUDITOR"]
    print(f"[INFO] User Roles: {user_roles}")
    
    effective_caps = set()
    for r in user_roles:
        caps = roles.get(r, [])
        effective_caps.update(caps)
        
    print(f"[INFO] Effective Capabilities: {sorted(list(effective_caps))}")
    
    # Verify expected union
    expected_agent = set(roles["AGENT"])
    expected_auditor = set(roles["AUDITOR"])
    
    if not expected_agent.issubset(effective_caps):
         print("[FAIL] Missing AGENT capabilities!")
         sys.exit(1)
    if not expected_auditor.issubset(effective_caps):
         print("[FAIL] Missing AUDITOR capabilities!")
         sys.exit(1)
         
    print("[PASS] Multi-Role correctly unioned capabilities.")

def main():
    try:
        test_multi_role_composition()
        print("\n[SUCCESS] Multi-Role Truth Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
