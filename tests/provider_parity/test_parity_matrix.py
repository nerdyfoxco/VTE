import json
import os
import sys

# Contract paths
PARITY_MATRIX_PATH = "contracts/provider/provider_parity_matrix_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def test_parity_matrix_structure():
    print("[INFO] Validating Provider Parity Matrix...")
    matrix_def = load_json(PARITY_MATRIX_PATH)
    
    matrix = matrix_def['matrix']
    if not matrix:
        print("[FAIL] Matrix is empty!")
        sys.exit(1)
        
    for provider, capabilities in matrix.items():
        print(f"  > Checking {provider}...")
        if 'features' not in capabilities:
             print(f"    [FAIL] {provider} missing 'features' list.")
             sys.exit(1)
        if 'limitations' not in capabilities:
             print(f"    [FAIL] {provider} missing 'limitations' list.")
             sys.exit(1)
             
    print("[PASS] Provider Parity Matrix is structurally valid.")

if __name__ == "__main__":
    try:
        test_parity_matrix_structure()
        print("\n[SUCCESS] Provider Parity Tests Passed.")
    except Exception as e:
        print(f"\n[ERROR] Test Failed: {e}")
        sys.exit(1)
