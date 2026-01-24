import json
import os
import sys

# Simulates Incident Timeline Reconstruction
# Merge logs from System, User, and Network into a single coherent timeline.

def test_incident_timeline():
    print("[INFO] Starting Incident Timeline Verification...")
    sys.path.append(os.getcwd())
    
    logs = [
        {"time": 10, "source": "USER", "msg": "Clicked Button"},
        {"time": 12, "source": "SYSTEM", "msg": "Error 500"},
        {"time": 11, "source": "NETWORK", "msg": "Request Sent"}
    ]
    
    print("  > Reconstructing timeline...")
    
    # Sort
    timeline = sorted(logs, key=lambda x: x["time"])
    
    expected_order = ["USER", "NETWORK", "SYSTEM"]
    actual_order = [x["source"] for x in timeline]
    
    print(f"    Timeline: {actual_order}")
    
    if actual_order == expected_order:
        print("    [PASS] Timeline reconstructed correctly.")
    else:
        print("    [FAIL] Timeline out of order.")
        sys.exit(1)

    print("\n[SUCCESS] Incident Timeline Scenario Proven.")

def main():
    try:
        test_incident_timeline()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
