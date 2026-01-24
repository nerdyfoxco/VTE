import json
import os
import sys

# Contract paths
BACKFILL_PROTOCOL_PATH = "contracts/migrations/backfill_protocol.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class ExecutionEngine:
    def __init__(self, backfill_protocol):
        self.protocol = backfill_protocol
        self.constraints = backfill_protocol['protocol']['constraints']
        self.side_effects_emitted = []

    def execute_event(self, event, run_mode):
        print(f"  > Executing event {event['id']} in mode {run_mode}...")
        
        # 1. Check Constraints
        if run_mode == "HISTORICAL_BACKFILL":
            constraint = self.constraints["HISTORICAL_BACKFILL"]
            
            # Check Side Effects
            if constraint["external_side_effects"] == "BLOCKED":
                if event.get("requires_external_call"):
                    print("    [BLOCK] External side effect suppressed by backfill protocol.")
                    return "SUPPRESSED"
            
        # 2. Execute (Simulated)
        if event.get("requires_external_call"):
            self.side_effects_emitted.append(event['id'])
            return "EXECUTED"
            
        return "PROCESSED_LOCAL"

def test_backfill_safety():
    print("[INFO] Loading Backfill Protocol...")
    protocol = load_json(BACKFILL_PROTOCOL_PATH)
    engine = ExecutionEngine(protocol)
    
    # Event definition
    test_event = {
        "id": "evt_123",
        "requires_external_call": True # e.g. send email
    }
    
    # 1. Test LIVE Mode (Should Emit)
    print("[INFO] Testing LIVE_PROCESSING mode...")
    result_live = engine.execute_event(test_event, "LIVE_PROCESSING")
    if result_live != "EXECUTED":
         print(f"[FAIL] Live mode suppressed side effect! Result: {result_live}")
         sys.exit(1)
    
    if "evt_123" not in engine.side_effects_emitted:
         print("[FAIL] Side effect not recorded in live mode.")
         sys.exit(1)
         
    # Reset
    engine.side_effects_emitted = []
    
    # 2. Test BACKFILL Mode (Should Suppress)
    print("[INFO] Testing HISTORICAL_BACKFILL mode...")
    result_backfill = engine.execute_event(test_event, "HISTORICAL_BACKFILL")
    
    if result_backfill != "SUPPRESSED":
         print(f"[FAIL] Backfill mode failed to suppress side effect! Result: {result_backfill}")
         sys.exit(1)

    if len(engine.side_effects_emitted) > 0:
         print("[FAIL] Side effect leaked during backfill!")
         sys.exit(1)

    print("[PASS] Backfill Safety Verified: Side effects blocked.")

def main():
    try:
        test_backfill_safety()
        print("\n[SUCCESS] Backfill Safety Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
