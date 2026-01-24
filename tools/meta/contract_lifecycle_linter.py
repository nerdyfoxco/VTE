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

def lint_contract(contract_path):
    print(f"[INFO] Linting {contract_path}...")
    try:
        contract = load_json(contract_path)
    except Exception as e:
        return False, f"JSON Error: {e}"
        
    policy = load_json(LIFECYCLE_POLICY_PATH)
    valid_states = set(policy['valid_states'])
    
    status = contract.get('status')
    if not status:
        return False, "Missing 'status' field."
        
    if status not in valid_states:
        return False, f"Invalid status '{status}'. Valid: {valid_states}"
        
    # Additional checks could go here (e.g. version format)
    return True, "Valid"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python contract_lifecycle_linter.py <CONTRACT_PATH>")
        sys.exit(1)
        
    path = sys.argv[1]
    valid, msg = lint_contract(path)
    if not valid:
        print(f"[FAIL] {msg}")
        sys.exit(1)
    else:
        print("[SUCCESS] Contract passes lifecycle checks.")
