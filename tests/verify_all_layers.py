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

    import subprocess
    
    # Ensure tests find the Seeded DB
    # We use relative path for CI/Local compatibility if possible, or keep the hardcode if user insists.
    # But for CI, absolute windows path is definitely wrong.
    # Ideally: db_path = "sqlite:///vte_backend.db" (since we are in spine dir).
    db_url = "sqlite:///vte_backend.db"

    env = os.environ.copy()
    env["DATABASE_URL"] = db_url
    
    # Use sys.executable to ensure we use the same python interpreter (within venv)
    print(f"RUNNING: {script_path} with {sys.executable}")
    
    try:
        subprocess.check_call([sys.executable, script_path], env=env)
        print(f"PASSED: {script_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: {script_path} exited with {e.returncode}")
        return False

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
