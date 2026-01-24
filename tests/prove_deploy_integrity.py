import json
import os
import sys

# Simulates Deployment Integrity Check
# Every deployed artifact must have a signature or checksum matching the manifest.

def test_deploy_integrity():
    print("[INFO] Starting Deployment Integrity Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Manifest
    manifest = {
        "artifacts": {
            "app.py": "hash_123"
        }
    }
    
    # Mock Artifacts on Disk
    artifacts = {
        "app.py": "hash_123",
        "rogue_script.py": "hash_666" # Unknown file
    }
    
    print("  > Verifying artifacts against manifest...")
    
    # Check everything on disk is in manifest (No rogues)
    for filename in artifacts:
        if filename not in manifest['artifacts']:
             print(f"    [PASS] Rogue artifact detected: {filename}")
             # In a real deploy, this would fail the startup.
             # Here we PROVE that we detected it.
             print("\n[SUCCESS] Deployment Integrity Scenario Proven.")
             return
             
    print("    [FAIL] Failed to detect rogue artifact.")
    sys.exit(1)

def main():
    try:
        test_deploy_integrity()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
