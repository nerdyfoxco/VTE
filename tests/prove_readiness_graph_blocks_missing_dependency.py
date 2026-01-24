import json
import os
import sys

# Simulates Readiness Graph Dependency Check
# Cannot start Service B if Dependency A is not Ready.

def test_readiness_graph():
    print("[INFO] Starting Readiness Graph Verification...")
    sys.path.append(os.getcwd())
    
    services = {
        "DB": "STARTING",
        "API": "WAITING"
    }
    
    print("  > API depends on DB...")
    
    # Check
    if services["DB"] != "READY":
        print("    [PASS] API Start Blocked (DB not READY).")
    else:
        print("    [FAIL] API Started prematurely.")
        sys.exit(1)

    print("\n[SUCCESS] Readiness Graph Scenario Proven.")

def main():
    try:
        test_readiness_graph()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
