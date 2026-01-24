import json
import os
import sys

# Contract paths
ATTRIBUTION_SCHEMA_PATH = "contracts/economics/cost_attribution_schema.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def validate_attribution(proof_run, schema):
    required = set(schema['schema']['required_tags'])
    allowed_centers = set(schema['schema']['cost_centers'])
    
    provided_tags = proof_run.get('cost_tags', {})
    
    # Check Required Tags
    for req in required:
        if req not in provided_tags:
            return False, f"Missing required tag: {req}"
            
    # Check Validity of Cost Center
    cc = provided_tags.get('cost_center')
    if cc and cc not in allowed_centers:
        return False, f"Invalid cost center: {cc}"
        
    return True, "Valid"

def test_cost_attribution():
    print("[INFO] Loading Cost Attribution Schema...")
    schema = load_json(ATTRIBUTION_SCHEMA_PATH)
    
    # 1. Valid Proof Run
    print("[INFO] Testing Valid Proof Run...")
    valid_run = {
        "proof_id": "prf_1",
        "cost_tags": {
            "tenant_id": "tenant_A",
            "cost_center": "PROCESSING",
            "feature_id": "ID_VERIFICATION"
        }
    }
    is_valid, msg = validate_attribution(valid_run, schema)
    if not is_valid:
        print(f"[FAIL] Valid run rejected: {msg}")
        sys.exit(1)
    print(f"[PASS] Valid run accepted.")
    
    # 2. Missing Tag
    print("[INFO] Testing Missing Tag Run...")
    invalid_run_missing = {
        "proof_id": "prf_2",
        "cost_tags": {
            "tenant_id": "tenant_A",
            # Missing cost_center
            "feature_id": "ID_VERIFICATION"
        }
    }
    is_valid, msg = validate_attribution(invalid_run_missing, schema)
    if is_valid:
        print(f"[FAIL] Run missing 'cost_center' was accepted!")
        sys.exit(1)
    print(f"[PASS] Missing tag correctly rejected: {msg}")

    # 3. Invalid Cost Center
    print("[INFO] Testing Invalid Cost Center Run...")
    invalid_run_cc = {
        "proof_id": "prf_3",
        "cost_tags": {
            "tenant_id": "tenant_A",
            "cost_center": "PARTY_PLANNING", # Invalid
            "feature_id": "ID_VERIFICATION"
        }
    }
    is_valid, msg = validate_attribution(invalid_run_cc, schema)
    if is_valid:
        print(f"[FAIL] Run with invalid cost center was accepted!")
        sys.exit(1)
    print(f"[PASS] Invalid cost center correctly rejected: {msg}")

def main():
    try:
        test_cost_attribution()
        print("\n[SUCCESS] Cost Attribution Enforcement Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
