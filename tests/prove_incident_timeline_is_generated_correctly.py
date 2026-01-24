import json
import os
import sys
import subprocess

# Paths
EMITTER_TOOL = "tools/ops/emit_incident_timeline.py"
CONTRACT_PATH = "contracts/ops/incident_timeline_export_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def test_timeline_integrity():
    print("[INFO] Testing Incident Timeline Emitter...")
    
    # 1. Load Contract Schema
    contract = load_json(CONTRACT_PATH)
    required = contract['schema']['required_fields']
    
    # 2. Run Emitter
    inc_id = "TEST-INC-123"
    res = subprocess.run(
        [sys.executable, EMITTER_TOOL, inc_id],
        capture_output=True,
        text=True
    )
    
    if res.returncode != 0:
        print(f"[FAIL] Emitter failed: {res.stderr}")
        sys.exit(1)
        
    try:
        timeline = json.loads(res.stdout)
    except json.JSONDecodeError:
        print(f"[FAIL] Invalid JSON output: {res.stdout}")
        sys.exit(1)
        
    # 3. Validate against Schema
    print("[INFO] Validating against contract...")
    for field in required:
        if field not in timeline:
            print(f"[FAIL] Missing required field: {field}")
            sys.exit(1)
            
    if timeline['incident_id'] != inc_id:
        print(f"[FAIL] Incident ID mismatch. Expected {inc_id} got {timeline['incident_id']}")
        sys.exit(1)
        
    events = timeline.get('events', [])
    if not events:
         print("[FAIL] No events in timeline!")
         sys.exit(1)
         
    print(f"[PASS] Timeline valid. Contains {len(events)} events.")

def main():
    try:
        test_timeline_integrity()
        print("\n[SUCCESS] Incident Timeline Integrity Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
