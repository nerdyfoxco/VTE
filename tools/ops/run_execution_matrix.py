import json
import os
import sys
import subprocess

# Paths
MATRIX_PATH = "contracts/ops/canary_execution_matrix_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def run_context(context_name):
    print(f"[INFO] Executing Matrix Context: {context_name}")
    matrix = load_json(MATRIX_PATH)
    
    if context_name not in matrix['contexts']:
         print(f"[FAIL] Unknown context: {context_name}")
         sys.exit(1)
         
    config = matrix['contexts'][context_name]
    canaries = config['required_canaries']
    blocking = config['blocking']
    
    failures = []
    
    for canary in canaries:
        if canary.endswith(".json"):
            # It's a contract, assume we just check existence for now
            if not os.path.exists(canary):
                failures.append(f"Missing Contract: {canary}")
            else:
                 print(f"  [PASS] Contract Exists: {canary}")
        elif canary.endswith(".py"):
             # Execute Test
             print(f"  > Running {canary}...")
             res = subprocess.run(
                 [sys.executable, canary],
                 capture_output=True,
                 text=True
             )
             if res.returncode != 0:
                 failures.append(f"Failed Canary {canary}: {res.stdout} {res.stderr}")
                 print(f"    [FAIL] Exit Code {res.returncode}")
             else:
                 print(f"    [PASS]")

    if failures:
        print(f"[ERROR] Context {context_name} had {len(failures)} failures.")
        if blocking:
             print("[BLOCK] Blocking Pipeline due to failures.")
             sys.exit(1)
        else:
             print("[WARN] Non-blocking failures detected.")
             sys.exit(0) # or 0 with warning

    print(f"[SUCCESS] Context {context_name} Clean.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_execution_matrix.py <CONTEXT_NAME>")
        sys.exit(1)
        
    ctx = sys.argv[1]
    run_context(ctx)
