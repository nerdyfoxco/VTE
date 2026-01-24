import json
import os
import sys

# Simulates Unknown Run Mode

def test_unknown_mode_negative():
    print("[INFO] Starting Unknown Mode Negative Verification...")
    sys.path.append(os.getcwd())
    
    # 1. Execution (Firewall)
    print("  > Phase 2: Execution (Firewall Mode Check)...")
    from tests.prove_firewall_blocks_undocumented_side_effects import Firewall, load_json as load_json_fw
    fw_policy = load_json_fw("contracts/execution/firewall_policy.json")
    registry = [{"handler_id": "call_handler", "side_effects": [{"type": "EXTERNAL_CALL"}]}]
    fw = Firewall(fw_policy, registry)
    
    # Attempt "GOD_MODE" (Unknown)
    perm = fw.check_permission("GOD_MODE", "call_handler", "EXTERNAL_CALL")
    
    if perm != "BLOCKED_UNKNOWN_MODE":
         print(f"    [FAIL] Expected BLOCKED_UNKNOWN_MODE, got {perm}")
         sys.exit(1)
         
    print("    [PASS] Unknown Mode Blocked.")
    print("\n[SUCCESS] Unknown Mode Negative Scenario Proven.")

def main():
    try:
        test_unknown_mode_negative()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
