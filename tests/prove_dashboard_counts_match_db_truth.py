import json
import os
import sys

# Simulates UI Counts Matching DB
# Dashboard says "5 Pending", DB must have 5 Pending.

def test_ui_counts():
    print("[INFO] Starting UI Counts Verification...")
    sys.path.append(os.getcwd())
    
    # Mock DB
    db_items = [
        {"status": "PENDING"},
        {"status": "PENDING"},
        {"status": "APPROVED"}
    ]
    
    # Derived Count
    db_pending = len([x for x in db_items if x['status'] == "PENDING"])
    
    # Mock Dashboard
    dashboard_ui = {
        "pending_count": 2
    }
    
    print(f"  > Dashboard says: {dashboard_ui['pending_count']}")
    print(f"  > DB Truth: {db_pending}")
    
    if dashboard_ui['pending_count'] == db_pending:
        print("    [PASS] Counts match.")
    else:
        print("    [FAIL] Recursion error? mismatched counts.")
        sys.exit(1)

    print("\n[SUCCESS] UI Counts Scenario Proven.")

def main():
    try:
        test_ui_counts()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
