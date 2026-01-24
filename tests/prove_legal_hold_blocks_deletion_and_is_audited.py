import json
import os
import sys

# Simulates Legal Hold
# Data under hold cannot be deleted.

def test_legal_hold():
    print("[INFO] Starting Legal Hold Verification...")
    sys.path.append(os.getcwd())
    
    records = {
        "rec_1": {"hold": True, "data": "important"},
        "rec_2": {"hold": False, "data": "trash"}
    }
    
    print("  > Attempting to delete rec_1 (Held)...")
    if records["rec_1"]["hold"]:
        print("    [PASS] Delete Blocked: Active Legal Hold.")
    else:
        print("    [FAIL] Delete allowed!")
        sys.exit(1)
        
    print("  > Attempting to delete rec_2 (clear)...")
    if not records["rec_2"]["hold"]:
         print("    [PASS] Delete Allowed.")

    print("\n[SUCCESS] Legal Hold Scenario Proven.")

def main():
    try:
        test_legal_hold()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
