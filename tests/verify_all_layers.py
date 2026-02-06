import os
import sys
import unittest
import importlib.util

# List of Verification Scripts
SCRIPTS = [
    "tests/verify_layer4_backend_logic.py",
    "tests/verify_layer4_bundle_loader.py",
    "tests/verify_layer5_concurrency.py",
    "tests/verify_layer8_observability.py",
    "tests/verify_layer9_admin.py"
]

def run_script(script_path):
    print(f"\n{'='*60}")
    print(f"RUNNING: {script_path}")
    print(f"{'='*60}")
    
    # Ensure tests find the Seeded DB
    # Real World: In CI this points to Service Container Postgres
    db_path = "sqlite:///c:/Bintloop/VTE/apps/backend-core/vte_backend.db"
    
    # Run via os.system to isolate environments roughly (simple harness)
    # in a real CI this would be pytest collection
    # We prepend env var setting (Windows syntax is different, so we simply set strict env in python)
    cmd = f"set DATABASE_URL={db_path} && python {script_path}"
    exit_code = os.system(cmd)
    
    if exit_code != 0:
        print(f"FAILED: {script_path} exited with {exit_code}")
        return False
    
    print(f"PASSED: {script_path}")
    return True

def main():
    print("STARTING FULL SYSTEM VERIFICATION SUITE")
    print(f"Targeting {len(SCRIPTS)} Layers...")
    
    failures = []
    for script in SCRIPTS:
        if not run_script(script):
            failures.append(script)
            
    print(f"\n{'='*60}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*60}")
    
    if failures:
        print(f"❌ FAILED ({len(failures)} scripts failed)")
        for f in failures:
            print(f" - {f}")
        sys.exit(1)
    else:
        print("✅ ALL SYSTEMS GREEN. VTE READY FOR SIGN-OFF.")
        sys.exit(0)

if __name__ == "__main__":
    main()
