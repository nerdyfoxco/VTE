import json
import os
import sys

def verify_runtime_layers():
    print("Verifying Layer 3 & 4: Runtime Layers...")
    
    # Paths
    frontend_path = os.path.join("apps", "frontend")
    backend_path = os.path.join("apps", "backend-core")
    spine_path = os.path.join(backend_path, "spine")
    bundle_policy_path = os.path.join("contracts", "meta", "bundle_only_runtime_policy_v1.json")
    
    # 1. Verify Frontend (Layer 3)
    if not os.path.isdir(frontend_path):
        print(f"FAIL: Frontend directory not found at {frontend_path}")
        sys.exit(1)
    
    # Check for package.json to confirm it's a JS project
    if not os.path.exists(os.path.join(frontend_path, "package.json")):
        print(f"FAIL: Frontend missing package.json")
        sys.exit(1)
        
    print("PASS: Frontend Runtime Layer (Physical) verified.")
    
    # 2. Verify Backend (Layer 4)
    if not os.path.isdir(backend_path):
        print(f"FAIL: Backend directory not found at {backend_path}")
        sys.exit(1)
        
    if not os.path.isdir(spine_path):
        print(f"FAIL: Spine module not found at {spine_path}")
        sys.exit(1)
        
    print("PASS: Backend Runtime Layer (Physical) verified.")
    
    # 3. Verify Bundle Execution Policy (Layer 4 Contract)
    if not os.path.exists(bundle_policy_path):
        print(f"FAIL: Bundle Only Runtime Policy not found at {bundle_policy_path}")
        sys.exit(1)
        
    try:
        with open(bundle_policy_path, 'r') as f:
            policy = json.load(f)
            print("PASS: Bundle Only Runtime Policy is valid JSON.")
            
        # Check basic fields
        if "policy_name" not in policy and "contract_name" not in policy:
             print("WARNING: Policy missing name field, but parsed OK.")
             
    except json.JSONDecodeError as e:
        print(f"FAIL: Bundle Only Runtime Policy invalid JSON: {e}")
        sys.exit(1)
        
    print("LAYER 3 & 4 VERIFIED.")

if __name__ == "__main__":
    verify_runtime_layers()
