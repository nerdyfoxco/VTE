import json
import os
import sys

def verify_layer2():
    print("Verifying Layer 2: User Surface...")
    
    # Paths
    ui_binding_path = os.path.join("contracts", "ux", "ui_action_binding_map_v1.json")
    unified_queue_path = os.path.join("contracts", "ux", "unified_queue_truth_v1.json")
    client_surfaces_path = os.path.join("contracts", "client_surfaces.json")
    
    # 1. Verify UI Action Binding Map
    if not os.path.exists(ui_binding_path):
        print(f"FAIL: UI Action Binding Map not found at {ui_binding_path}")
        sys.exit(1)
        
    try:
        with open(ui_binding_path, 'r') as f:
            bindings = json.load(f)
            print("PASS: UI Action Binding Map is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: UI Action Binding Map invalid JSON: {e}")
        sys.exit(1)
        
    if "bindings" not in bindings:
        print("FAIL: binding map missing 'bindings' list")
        sys.exit(1)
        
    # Check for duplicate UI Element IDs
    seen_ids = set()
    for b in bindings["bindings"]:
        ui_id = b.get("ui_element_id")
        if not ui_id:
            print("FAIL: Binding entry missing 'ui_element_id'")
            sys.exit(1)
        if ui_id in seen_ids:
             print(f"FAIL: Duplicate ui_element_id found: {ui_id}")
             sys.exit(1)
        seen_ids.add(ui_id)
        
        if "required_contract" not in b:
            print(f"FAIL: Binding for {ui_id} missing 'required_contract'")
            sys.exit(1)
            
    print("PASS: UI Action Binding Map structural integrity verified.")

    # 2. Verify Unified Queue Truth
    if not os.path.exists(unified_queue_path):
        # This might be missing based on my previous broad searches
        print(f"WARNING: Unified Queue Truth not found at {unified_queue_path}. Verifying if this is acceptable...")
        # If it's strictly required by L2 definition, this is a FAIL.
        # But let's check if the file really exists first via the script logic.
        print(f"FAIL: Unified Queue Truth contract missing.")
        sys.exit(1) 
        
    try:
        with open(unified_queue_path, 'r') as f:
            queue = json.load(f)
            print("PASS: Unified Queue Truth is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Unified Queue Truth invalid JSON: {e}")
        sys.exit(1)

    # 3. Verify Client Surfaces (Kevin)
    if not os.path.exists(client_surfaces_path):
        print(f"FAIL: Client Surfaces map not found at {client_surfaces_path}")
        sys.exit(1)
        
    try:
        with open(client_surfaces_path, 'r') as f:
            surfaces = json.load(f)
            print("PASS: Client Surfaces map is valid JSON.")
            
        # Check for 'kevin' or relevant persona
        # Reading file content would confirm structure, but basic JSON check is start.
    except json.JSONDecodeError as e:
        print(f"FAIL: Client Surfaces map invalid JSON: {e}")
        sys.exit(1)

    print("LAYER 2 VERIFIED.")

if __name__ == "__main__":
    verify_layer2()
