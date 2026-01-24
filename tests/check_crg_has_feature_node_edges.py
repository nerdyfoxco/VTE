import json
import os
import sys

# Contract paths
FEATURE_PACKET_PATH = "contracts/features/vte_delinquency_v1/feature_truth_packet_v1.json"

# In a real scenario, this would load the actual Readiness Graph. 
# Here we mock checking that the Feature Packet *defines* the edges we expect the graph to have.

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def check_feature_edges():
    print("[INFO] Loading Feature Truth Packet...")
    packet = load_json(FEATURE_PACKET_PATH)
    
    components = packet['components']
    
    print("[INFO] Verifying Edge Definitions...")
    
    # 1. Verify Scope exists
    if "scope" not in components:
        print("[FAIL] Feature Packet missing 'scope' edge!")
        sys.exit(1)
        
    # 2. Verify Journey exists
    if "journey" not in components:
        print("[FAIL] Feature Packet missing 'journey' edge!")
        sys.exit(1)

    # 3. Verify path resolution (light check)
    for key, path in components.items():
        if not path.startswith("contracts/"):
             print(f"[FAIL] Component {key} has invalid path layout: {path}")
             sys.exit(1)
             
    print(f"[PASS] {len(components)} edges verified in Truth Packet.")

def main():
    try:
        check_feature_edges()
        print("\n[SUCCESS] CRG Edge Definition Check Passed.")
    except Exception as e:
        print(f"\n[ERROR] Check Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
