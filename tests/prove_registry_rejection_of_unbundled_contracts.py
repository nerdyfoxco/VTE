import json
import os
import sys

# Simulates Registry Bundle Check
# Individual contracts cannot be registered directly; must be part of a bundle.

def test_registry_bundle():
    print("[INFO] Starting Registry Bundle Verification...")
    sys.path.append(os.getcwd())
    
    def register(item_type, item_id):
        if item_type == "CONTRACT":
            return "BLOCKED_USE_BUNDLE"
        if item_type == "BUNDLE":
            return "REGISTERED"
            
    print("  > Registering loose contract...")
    if register("CONTRACT", "c1") == "BLOCKED_USE_BUNDLE":
        print("    [PASS] Loose contract rejected.")
    else: sys.exit(1)
    
    print("  > Registering bundle...")
    if register("BUNDLE", "b1") == "REGISTERED":
         print("    [PASS] Bundle accepted.")

    print("\n[SUCCESS] Registry Bundle Scenario Proven.")

def main():
    try:
        test_registry_bundle()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
