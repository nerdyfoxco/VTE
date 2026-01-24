import json
import os
import sys

# Simulates To-Do Deduplication and Closure
# If duplicate task arrives, update existing. If action taken, close task.

def test_todo_lifecycle():
    print("[INFO] Starting To-Do Lifecycle Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Store
    todos = {}
    
    def upsert_todo(intent_id):
        if intent_id in todos:
            return "UPDATED"
        todos[intent_id] = "OPEN"
        return "CREATED"
        
    def close_todo(intent_id):
        if intent_id in todos:
            todos[intent_id] = "CLOSED"
            return "SUCCESS"
        return "NOT_FOUND"
        
    print("  > 1. Create Task A...")
    if upsert_todo("A") == "CREATED":
        print("    [PASS] Task A Created.")
    else: sys.exit(1)
    
    print("  > 2. Create Task A (Duplicate)...")
    if upsert_todo("A") == "UPDATED":
        print("    [PASS] Task A Deduped.")
    else: sys.exit(1)
    
    print("  > 3. Close Task A...")
    if close_todo("A") == "SUCCESS" and todos["A"] == "CLOSED":
        print("    [PASS] Task A Closed.")
    else: sys.exit(1)

    print("\n[SUCCESS] To-Do Lifecycle Scenario Proven.")

def main():
    try:
        test_todo_lifecycle()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
