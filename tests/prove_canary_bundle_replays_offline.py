import json
import os
import sys

# Contract and Harness
HARNESS_PATH = "tests/canary_harness/harness.py"

def test_offline_replay():
    print("[INFO] Setting up offline replay bundle...")
    
    # 1. Create a dummy script
    script_path = "tests/temp_dummy_canary.py"
    with open(script_path, "w") as f:
        f.write("print('Dummy running')")
        
    # 2. Create a bundle
    bundle = {
        "bundle_id": "test-bundle-1",
        "canary_script_path": script_path,
        "inputs": {},
        "expected_output_hash": "skip",
        "required_mode": "REPLAY"
    }
    
    bundle_path = "tests/temp_bundle.json"
    with open(bundle_path, "w") as f:
        json.dump(bundle, f)
        
    # 3. Invoke Harness (Importing class directly)
    sys.path.append(os.getcwd())
    from tests.canary_harness.harness import CanaryHarness
    
    print("  > Running Harness in OFFLINE mode...")
    harness = CanaryHarness(bundle_path)
    res = harness.run(mode_override="OFFLINE")
    
    if res != "SUCCESS":
        print(f"[FAIL] Expected SUCCESS, got {res}")
        # Cleanup
        os.remove(script_path)
        os.remove(bundle_path)
        sys.exit(1)
        
    print("[PASS] Offline replay executed successfully.")
    
    # 4. Cleanup
    os.remove(script_path)
    os.remove(bundle_path)

def main():
    try:
        test_offline_replay()
        print("\n[SUCCESS] Offline Replay Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
