import json
import os
import sys

def verify_final_layers():
    print("Verifying Layer 8, 10 & 11: Observability, Tenancy & Completion...")
    
    # Paths
    observability_path = os.path.join("contracts", "ops", "observability_policy_v1.json")
    tenancy_path = os.path.join("contracts", "tenancy_model.json")
    signoff_path = os.path.join("contracts", "meta", "final_signoff_sheet.md")
    dod_path = os.path.join("contracts", "meta", "dod_vte_phase0.md")
    
    # 1. Verify Observability (Layer 8)
    if not os.path.exists(observability_path):
        print(f"FAIL: Observability Policy not found at {observability_path}")
        sys.exit(1)
        
    try:
        with open(observability_path, 'r') as f:
            json.load(f)
            print("PASS: Observability Policy is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Observability Policy invalid JSON: {e}")
        sys.exit(1)

    # 2. Verify Environment Ownership / Tenancy (Layer 10)
    if not os.path.exists(tenancy_path):
        print(f"FAIL: Tenancy Model not found at {tenancy_path}")
        sys.exit(1)
        
    try:
        with open(tenancy_path, 'r') as f:
            t = json.load(f)
            print("PASS: Tenancy Model is valid JSON.")
            if t.get("schema") != "vte_tenancy_model_v1":
                print("FAIL: Tenancy Model schema mismatch")
                sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"FAIL: Tenancy Model invalid JSON: {e}")
        sys.exit(1)

    # 3. Verify Product Completion (Layer 11)
    if not os.path.exists(signoff_path):
        print(f"FAIL: Final Signoff Sheet not found at {signoff_path}")
        sys.exit(1)
        
    if not os.path.exists(dod_path):
        print(f"FAIL: DoD Phase 0 not found at {dod_path}")
        sys.exit(1)
        
    print("PASS: Completion contracts (Markdown) exist.")
    print("LAYER 8, 10 & 11 VERIFIED.")

if __name__ == "__main__":
    verify_final_layers()
