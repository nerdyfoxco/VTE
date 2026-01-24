import json
import os
import sys
import subprocess

# Paths
VALIDATOR_TOOL = "tools/ops/validate_canary_matrix.py"
MATRIX_PATH = "contracts/ops/canary_execution_matrix_v1.json"

def test_coverage_enforcement():
    print("[INFO] Testing Matrix Coverage Enforcement...")
    
    # 1. Test Valid Matrix (current)
    res = subprocess.run(
        [sys.executable, VALIDATOR_TOOL],
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        print(f"[FAIL] Valid matrix failed: {res.stdout}")
        sys.exit(1)
    print("[PASS] Valid matrix accepted.")
    
    # 2. Test Missing Coverage (Mock)
    # Load and strip Golden Journey from Pre-deploy
    with open(MATRIX_PATH, 'r') as f:
        matrix = json.load(f)
        
    original = matrix['contexts']['PRE_DEPLOY']['required_canaries']
    # Removing golden journey
    filtered = [c for c in original if "golden_journey" not in c]
    matrix['contexts']['PRE_DEPLOY']['required_canaries'] = filtered
    
    with open("temp_matrix_missing.json", "w") as f:
        json.dump(matrix, f)
        
    # Hack: Pass temp file path via monkeypatch or redirect logic?
    # Our validator tool hardcodes the path for now. 
    # Let's temporarily swap the file.
    os.rename(MATRIX_PATH, MATRIX_PATH + ".bak")
    os.rename("temp_matrix_missing.json", MATRIX_PATH)
    
    try:
        res = subprocess.run(
            [sys.executable, VALIDATOR_TOOL],
            capture_output=True,
            text=True
        )
        
        if res.returncode == 0:
             print("[FAIL] Validator accepted matrix with missing Golden Journey coverage!")
             sys.exit(1)
             
        if "PRE_DEPLOY missing Golden Journey Coverage" not in res.stdout:
             print(f"[FAIL] Unexpected error message: {res.stdout}")
             sys.exit(1)
             
        print("[PASS] Validator blocked missing coverage.")
        
    finally:
        # Restore
        if os.path.exists(MATRIX_PATH + ".bak"):
            if os.path.exists(MATRIX_PATH):
                os.remove(MATRIX_PATH)
            os.rename(MATRIX_PATH + ".bak", MATRIX_PATH)

def main():
    try:
        test_coverage_enforcement()
        print("\n[SUCCESS] Matrix Coverage Enforcement Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
