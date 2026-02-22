import json
import os
import sys

def verify_release_gov():
    print("Verifying Layer 7 & 9: Release & Governance...")
    
    # Paths
    provenance_path = os.path.join("contracts", "deploy", "provenance_enforcement_policy.json")
    ship_gate_path = os.path.join("contracts", "release", "ship_gate_binding_v1.json")
    identity_path = os.path.join("contracts", "iam", "identity_admin_surface_v1.json")
    repo_policy_path = os.path.join("contracts", "meta", "repo_access_policy.md")
    
    # 1. Verify Deployment/Release (Layer 7)
    if not os.path.exists(provenance_path):
        print(f"FAIL: Provenance Policy not found at {provenance_path}")
        sys.exit(1)
        
    try:
        with open(provenance_path, 'r') as f:
            json.load(f)
            print("PASS: Provenance Policy is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Provenance Policy invalid JSON: {e}")
        sys.exit(1)
        
    if not os.path.exists(ship_gate_path):
        print(f"FAIL: Ship Gate Binding not found at {ship_gate_path}")
        sys.exit(1)

    try:
        with open(ship_gate_path, 'r') as f:
            json.load(f)
            print("PASS: Ship Gate Binding is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Ship Gate Binding invalid JSON: {e}")
        sys.exit(1)

    # 2. Verify Governance (Layer 9)
    if not os.path.exists(identity_path):
         print(f"FAIL: Identity Admin Surface not found at {identity_path}")
         sys.exit(1)
         
    try:
        with open(identity_path, 'r') as f:
            json.load(f)
            print("PASS: Identity Admin Surface is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Identity Admin Surface invalid JSON: {e}")
        sys.exit(1)
        
    if not os.path.exists(repo_policy_path):
        print(f"FAIL: Repo Access Policy not found at {repo_policy_path}")
        sys.exit(1)
        
    print("PASS: Repo Access Policy (Markdown) exists.")
    print("LAYER 7 & 9 VERIFIED.")

if __name__ == "__main__":
    verify_release_gov()
