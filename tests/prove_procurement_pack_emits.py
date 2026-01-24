import json
import os
import sys
import subprocess

# Paths
EMITTER_PATH = "tools/procurement/emit_security_package.py"
INDEX_PATH = "contracts/procurement/security_package_index.json"
SOD_CONTRACT = "contracts/security/separation_of_duties_v1.json" # Expected to exist

def test_package_emitter():
    print("[INFO] Testing Security Package Emitter...")
    
    # 1. Run the emitter tool via subprocess to verify CLI contract
    try:
        result = subprocess.run(
            [sys.executable, EMITTER_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        output_json = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Emitter execution failed: {e.stderr}")
        sys.exit(1)

    # 2. Parse Output
    try:
        package = json.loads(output_json)
    except json.JSONDecodeError:
         print(f"[FAIL] Emitter produced invalid JSON: {output_json}")
         sys.exit(1)
         
    # 3. Verify Integrity Structure
    if "integrity_hash" not in package:
         print("[FAIL] Missing 'integrity_hash'!")
         sys.exit(1)
         
    artifacts = package['manifest']['artifacts']
    print(f"[INFO] Generated manifest with {len(artifacts)} sections.")
    
    # 4. Verify Content (Spot Check SOD)
    sod_artifact = artifacts.get('governance', {}).get('separation_of_duties', {})
    if sod_artifact.get('path') != SOD_CONTRACT:
         print(f"[FAIL] Separation of duties path mismatch! Got: {sod_artifact.get('path')}")
         sys.exit(1)
         
    if sod_artifact.get('status') != "PRESENT":
         # It might be MISSING if we didn't run the previous phases fully in this environment, 
         # but we know we made it in Phase 1.11.
         print(f"[FAIL] Separation of duties contract reported as MISSING! (Should exist)")
         sys.exit(1)

    print("[PASS] Security Package Emitter produces valid, verified output.")

def main():
    try:
        test_package_emitter()
        print("\n[SUCCESS] Procurement Pack Integrity Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
