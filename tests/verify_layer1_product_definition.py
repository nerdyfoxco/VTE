import json
import os
import sys

def verify_layer1():
    print("Verifying Layer 1: Product Definition...")
    
    # Paths
    scope_path = os.path.join("contracts", "features", "vte_delinquency_v1", "scope_contract.json")
    boundary_path = os.path.join("contracts", "product", "product_boundary_map.json")
    
    # 1. Verify Scope Contract Exists and is Valid JSON
    if not os.path.exists(scope_path):
        print(f"FAIL: Scope contract not found at {scope_path}")
        sys.exit(1)
        
    try:
        with open(scope_path, 'r') as f:
            scope = json.load(f)
            print("PASS: Scope contract is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Scope contract invalid JSON: {e}")
        sys.exit(1)
        
    # 2. Verify Key Fields in Scope Contract
    required_fields = ["feature_id", "states", "transitions", "side_effects", "invariants"]
    for field in required_fields:
        if field not in scope:
            print(f"FAIL: Scope contract missing required field: {field}")
            sys.exit(1)
    print("PASS: Scope contract contains all required fields.")
    
    # 3. Verify Product Boundary Map
    if not os.path.exists(boundary_path):
        print(f"FAIL: Product boundary map not found at {boundary_path}")
        sys.exit(1)
        
    try:
        with open(boundary_path, 'r') as f:
            boundary = json.load(f)
            print("PASS: Product boundary map is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Product boundary map invalid JSON: {e}")
        sys.exit(1)
        
    # 4. Verify Feature is Mapped in Boundary
    feature_id = scope["feature_id"]
    if "delinquency_feature" not in boundary["boundaries"]:
         print(f"FAIL: 'delinquency_feature' not found in product boundaries.")
         sys.exit(1)
         
    print(f"PASS: Feature '{feature_id}' is structurally accounted for in product definitions.")

    # 5. Verify Feature Truth Packet (T-0001)
    packet_path = os.path.join("contracts", "features", "vte_delinquency_v1", "feature_truth_packet_v1.json")
    if not os.path.exists(packet_path):
        print(f"FAIL: Feature Truth Packet not found at {packet_path}")
        sys.exit(1)
        
    try:
        with open(packet_path, 'r') as f:
            packet = json.load(f)
            print("PASS: Feature Truth Packet is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Feature Truth Packet invalid JSON: {e}")
        sys.exit(1)
        
    # Check T-0001 Acceptance Criteria
    failed_criteria = []
    
    # "Packet enumerates every allowed irreversible action"
    if "irreversible_actions" not in packet:
        failed_criteria.append("Missing 'irreversible_actions' section")
    
    # "Packet specifies evidence ladder minimum per step"
    if "evidence_ladder" not in packet:
        failed_criteria.append("Missing 'evidence_ladder' section")
        
    # "Packet binds state machine(s)"
    if "state_machine_binding" not in packet:
        failed_criteria.append("Missing 'state_machine_binding' section")
        
    # "Packet declares idempotency keys"
    if "idempotency_keys" not in packet:
        failed_criteria.append("Missing 'idempotency_keys' section")
        
    if failed_criteria:
        print(f"FAIL: Feature Truth Packet missing acceptance criteria: {', '.join(failed_criteria)}")
        sys.exit(1)
        
    print("PASS: Feature Truth Packet meets structural acceptance criteria.")
    print("LAYER 1 VERIFIED.")

if __name__ == "__main__":
    verify_layer1()
