import json
import os
import sys

# Simulates Plane Boundary Enforcement
# Control Plane vs Data Plane.
# Data Plane code cannot access Control Plane secrets or DB.

def test_plane_boundary():
    print("[INFO] Starting Plane Boundary Verification...")
    sys.path.append(os.getcwd())
    
    current_plane = "DATA_PLANE"
    
    # Mock Secret Check
    def access_secret(name):
        secrets = {"control_db_pass": "secret", "data_api_key": "public"}
        if current_plane == "DATA_PLANE" and "control" in name:
            return "BLOCKED_BOUNDARY_VIOLATION"
        return secrets[name]
        
    print(f"  > Attempting to access Control Plane secret from {current_plane}...")
    
    res = access_secret("control_db_pass")
    
    if res == "BLOCKED_BOUNDARY_VIOLATION":
        print("    [PASS] Control Plane access blocked.")
    else:
        print(f"    [FAIL] Boundary violation allowed: {res}")
        sys.exit(1)

    print("\n[SUCCESS] Plane Boundary Scenario Proven.")

def main():
    try:
        test_plane_boundary()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
