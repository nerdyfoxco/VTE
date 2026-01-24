import json
import os
import sys

# Simulates Code Drift (Function signature doesn't match registry)
# For this VTE, code drift is often detected by registry or firewall mismatch.
# Registry says handler "call_handler" does "EXTERNAL_CALL".
# If code tries "DB_WRITE", it drifts from registry.

def test_drift_negative():
    print("[INFO] Starting Drift Negative Verification...")
    sys.path.append(os.getcwd())
    
    # 1. Execution (Firewall)
    print("  > Phase 2: Execution (Firewall Drift Check)...")
    from tests.prove_firewall_blocks_undocumented_side_effects import Firewall, load_json as load_json_fw
    fw_policy = load_json_fw("contracts/execution/firewall_policy.json")
    registry = [{"handler_id": "call_handler", "side_effects": [{"type": "EXTERNAL_CALL"}]}]
    fw = Firewall(fw_policy, registry)
    
    # Attempt DB_WRITE (Not in registry for this handler)
    perm = fw.check_permission("LIVE", "call_handler", "DB_WRITE")
    
    if perm != "BLOCKED_UNDOCUMENTED_SIDE_EFFECT":
         print(f"    [FAIL] Expected BLOCKED_UNDOCUMENTED_SIDE_EFFECT, got {perm}")
         sys.exit(1)
         
    print("    [PASS] Drifting Side Effect Blocked.")
    print("\n[SUCCESS] Drift Negative Scenario Proven.")

def main():
    try:
        test_drift_negative()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
