import json
import os
import sys
import subprocess

# Paths
VALIDATOR_TOOL = "tools/meta/validate_wiring_reachability.py"

def test_orphan_detection():
    print("[INFO] Running Wiring Validator (expecting orphan detection)...")
    
    # We expect the tool (as implemented previously) to fail because "vte.unused.handler" is orphaned
    # and the rule "no_orphan_handlers" is true.
    
    res = subprocess.run(
        [sys.executable, VALIDATOR_TOOL],
        capture_output=True,
        text=True
    )
    
    if res.returncode == 0:
        print("[FAIL] Validator passed despite orphan handler!")
        sys.exit(1)
        
    if "Orphan Handlers Detected" not in res.stdout:
         print(f"[FAIL] Expected Orphan error, got: {res.stdout}")
         sys.exit(1)
         
    print("[PASS] Orphan Function correctly detected and blocked.")

def main():
    try:
        test_orphan_detection()
        print("\n[SUCCESS] Unreachable Function Detection Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
