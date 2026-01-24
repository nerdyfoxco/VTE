import json
import os
import sys
import subprocess

# Paths
VALIDATOR_TOOL = "tools/meta/validate_readiness_graph.py"
GRAPH_PATH_V1 = "contracts/meta/readiness_graph_v1.json"

def test_graph_validation():
    print("[INFO] Testing Valid Graph...")
    res = subprocess.run(
        [sys.executable, VALIDATOR_TOOL, GRAPH_PATH_V1],
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        print(f"[FAIL] Valid graph failed validation! {res.stdout} {res.stderr}")
        sys.exit(1)
    print("[PASS] Valid graph passed.")

    # Create Invalid Graph Temporary
    invalid_graph = {
        "nodes": [
            {"id": "n1", "type": "UNKNOWN_TYPE", "metadata": {}}
        ],
        "edges": []
    }
    with open("temp_invalid_graph.json", "w") as f:
        json.dump(invalid_graph, f)
        
    print("[INFO] Testing Invalid Graph...")
    res = subprocess.run(
        [sys.executable, VALIDATOR_TOOL, "temp_invalid_graph.json"],
        capture_output=True,
        text=True
    )
    
    # Cleanup
    os.remove("temp_invalid_graph.json")
    
    if res.returncode == 0:
        print("[FAIL] Invalid graph passed validation!")
        sys.exit(1)
    
    if "Unknown Node Type" not in res.stdout:
         print(f"[FAIL] Expected 'Unknown Node Type' error, got: {res.stdout}")
         sys.exit(1)

    print("[PASS] Invalid graph correctly rejected.")

def main():
    try:
        test_graph_validation()
        print("\n[SUCCESS] Graph Validation Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
