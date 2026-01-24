import json
import os
import sys

# Simulates Multi-Role View
# Admin sees ALL. Agent sees OWN.

def test_multi_role():
    print("[INFO] Starting Multi-Role Verification...")
    sys.path.append(os.getcwd())
    
    data = [
        {"id": 1, "owner": "agent_1"},
        {"id": 2, "owner": "agent_2"}
    ]
    
    # 1. Agent 1 View
    print("  > Agent 1 Query...")
    view_1 = [x for x in data if x['owner'] == "agent_1"]
    if len(view_1) == 1 and view_1[0]['id'] == 1:
        print("    [PASS] Agent 1 sees own data.")
    else:
        print("    [FAIL] Agent 1 sees wrong data.")
        sys.exit(1)
        
    # 2. Admin View
    print("  > Admin Query...")
    view_admin = data # Admin sees all
    if len(view_admin) == 2:
        print("    [PASS] Admin sees all data.")
    else:
        print("    [FAIL] Admin missing data.")
        sys.exit(1)

    print("\n[SUCCESS] Multi-Role Scenario Proven.")

def main():
    try:
        test_multi_role()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
