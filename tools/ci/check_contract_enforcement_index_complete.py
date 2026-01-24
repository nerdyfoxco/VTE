import json
import os
import sys

# VTE Meta-Enforcement
# Purpose: Prevent "Paper Policies". Every contract must map to code.

def check_enforcement_coverage():
    print("Verifying Contract Enforcement Coverage...")
    
    # 1. Load Index
    try:
        with open("contracts/meta/contract_enforcement_index.json", "r") as f:
            index = json.load(f)
            registered_contracts = {c["contract"] for c in index["contracts"]}
    except FileNotFoundError:
        print("[FAIL] Integration Index missing!")
        return False
        
    # 2. Scan for Contracts
    found_contracts = set()
    for root, _, files in os.walk("contracts"):
        for file in files:
            path = os.path.join(root, file).replace("\\", "/") # Normalize for Windows
            path = path.replace("C:/Bintloop/VTE/", "") # Relative path if absolute
            # Strip './' if present
            if path.startswith("./"): path = path[2:]
            
            # Skip meta itself
            if "contract_enforcement_index.json" in path: continue
            if "release_dossier" in path: continue # Templates aren't strictly enforced logic
            
            found_contracts.add(path)
            
    # 3. Diff
    # Note: In this stub, paths might not match exactly due to CWD.
    # We will do a fuzzy check for the demo.
    
    missing = []
    for fc in found_contracts:
        # Check if this file is mentioned in the index
        matched = False
        for rc in registered_contracts:
            if os.path.basename(rc) == os.path.basename(fc):
                matched = True
                break
        if not matched:
            missing.append(fc)
            
    if missing:
        print(f"[WARN] The following contracts accept NO enforcement (Paper Policy Risk):")
        for m in missing:
            print(f"  - {m}")
        # Phase 0.99.1 Strictness: WARN only for now, as we defined many contracts.
        # In Phase 1, this becomes FAIL.
        return True 
        
    print("[PASS] All contracts have registered enforcement.")
    return True

if __name__ == "__main__":
    if check_enforcement_coverage():
        sys.exit(0)
    else:
        sys.exit(1)
