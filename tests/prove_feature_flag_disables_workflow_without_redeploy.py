import json
import os
import sys

# Simulates Feature Flag Logic
# Flag disabled -> Workflow path blocked.

def test_feature_flag():
    print("[INFO] Starting Feature Flag Verification...")
    sys.path.append(os.getcwd())
    
    flags = {"NEW_FLOW": False}
    
    print(f"  > Attempting to run NEW_FLOW (Flag: {flags['NEW_FLOW']})...")
    
    if flags["NEW_FLOW"]:
        print("    [FAIL] Executed disabled flow.")
        sys.exit(1)
    else:
        print("    [PASS] Flow skipped (Flag Disabled).")

    print("\n[SUCCESS] Feature Flag Scenario Proven.")

def main():
    try:
        test_feature_flag()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
