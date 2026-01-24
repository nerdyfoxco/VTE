import json
import os
import sys

# Contract paths
MATRIX_PATH = "contracts/ops/canary_execution_matrix_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def validate_matrix():
    print("[INFO] Validating Canary Execution Matrix...")
    matrix = load_json(MATRIX_PATH)
    
    contexts = matrix['contexts']
    constraints = matrix.get('constraints', {})
    
    # 1. Validate Paths Exist (or at least defined)
    for ctx, config in contexts.items():
        print(f"  > Context: {ctx}")
        for path in config['required_canaries']:
            # Allow contract refs or py files
            if not (path.endswith(".json") or path.endswith(".py")):
                return False, f"Invalid canary reference: {path}"
            
            # Warn if missing locally (might be dynamic)
            if not os.path.exists(path):
                 print(f"    [WARN] Canary file missing locally: {path}")

    # 2. Check Constraints
    coverage_rule = constraints.get("coverage_minimum")
    if coverage_rule == "GOLDEN_JOURNEY_MUST_RUN_IN_PRE_DEPLOY":
        pre_deploy = contexts.get("PRE_DEPLOY", {})
        golden_found = False
        for path in pre_deploy.get("required_canaries", []):
            if "golden_journey" in path:
                golden_found = True
                break
        
        if not golden_found:
            return False, "PRE_DEPLOY missing Golden Journey Coverage!"

    return True, "Matrix Valid"

if __name__ == "__main__":
    valid, msg = validate_matrix()
    if not valid:
        print(f"[FAIL] {msg}")
        sys.exit(1)
    print(f"[SUCCESS] {msg}")
