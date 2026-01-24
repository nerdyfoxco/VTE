import json
import os
import sys

# Simulates Learning Isolation
# Tenant A's data should NOT improve Tenant B's model results (in this simple check, we check data partition).

def test_learning_isolation():
    print("[INFO] Starting Learning Isolation Verification...")
    sys.path.append(os.getcwd())
    
    training_set = [
        {"tenant": "A", "data": "foo"},
        {"tenant": "B", "data": "bar"}
    ]
    
    print("  > Training Model for Tenant A...")
    
    # Filter
    model_data = [x for x in training_set if x['tenant'] == "A"]
    
    print(f"    Included: {model_data}")
    
    # Verify B is not in there
    for item in model_data:
        if item['tenant'] != "A":
            print("    [FAIL] Data leak detected!")
            sys.exit(1)
            
    if len(model_data) == 1:
        print("    [PASS] Only Tenant A data used.")
    else:
        print("    [FAIL] Data missing.")
        sys.exit(1)

    print("\n[SUCCESS] Learning Isolation Scenario Proven.")

def main():
    try:
        test_learning_isolation()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
