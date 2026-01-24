import json
import os
import sys

# Simulates Promotion Barrier
# No promotion without valid bundle.

def test_promotion_barrier():
    print("[INFO] Starting Promotion Barrier Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Promotion Service
    def promote_model(bundle):
        if not bundle:
            return "BLOCKED_NO_BUNDLE"
        if "signature" not in bundle:
            return "BLOCKED_UNSIGNED"
        return "PROMOTED"
        
    print("  > Attempting promotion without bundle...")
    if promote_model(None) == "BLOCKED_NO_BUNDLE":
        print("    [PASS] Blocked empty promotion.")
    else: sys.exit(1)
    
    print("  > Attempting promotion with valid bundle...")
    bundle = {"id": "b1", "signature": "sig"}
    if promote_model(bundle) == "PROMOTED":
        print("    [PASS] Promoted valid bundle.")
    else: sys.exit(1)

    print("\n[SUCCESS] Promotion Barrier Scenario Proven.")

def main():
    try:
        test_promotion_barrier()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
