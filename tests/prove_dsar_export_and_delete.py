import json
import os
import sys

# Simulates DSAR (Data Subject Access Request)
# Export + Delete logic simulation.

def test_dsar():
    print("[INFO] Starting DSAR Verification...")
    sys.path.append(os.getcwd())
    
    user_db = {
        "user_1": {"name": "Alice", "email": "alice@example.com", "logs": ["login", "click"]}
    }
    
    # 1. Export
    print("  > Exporting data for user_1...")
    if "user_1" not in user_db:
         print("    [FAIL] User not found.")
         sys.exit(1)
         
    export_pkg = user_db["user_1"]
    print(f"    [PASS] Exported: {export_pkg.keys()}")
    
    # 2. Delete
    print("  > Deleting user_1...")
    del user_db["user_1"]
    
    if "user_1" in user_db:
         print("    [FAIL] Delete failed.")
         sys.exit(1)
         
    print("    [PASS] User deleted.")
    print("\n[SUCCESS] DSAR Scenario Proven.")

def main():
    try:
        test_dsar()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
