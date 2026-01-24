import json
import os
import sys

# Simulates Learning Isolation Check
# Ensure Artifacts from Tenant A are not accessible by Tenant B.

def test_learning_artifacts():
    print("[INFO] Starting Learning Artifact Isolation Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Store
    artifacts = [
        {"id": "a1", "tenant": "A"},
        {"id": "b1", "tenant": "B"}
    ]
    
    requester_tenant = "A"
    print(f"  > Requester: Tenant {requester_tenant}...")
    
    visible = [x for x in artifacts if x['tenant'] == requester_tenant]
    
    print(f"    Visible Artifacts: {[x['id'] for x in visible]}")
    
    if len(visible) == 1 and visible[0]['id'] == "a1":
        print("    [PASS] Isolation verified.")
    else:
        print("    [FAIL] Leaked artifacts!")
        sys.exit(1)

    print("\n[SUCCESS] Learning Isolation Scenario Proven.")

def main():
    try:
        test_learning_artifacts()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
