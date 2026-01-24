import json
import os
import sys

# Simulates a Replay mode properly blocking side effects

def test_replay_negative():
    print("[INFO] Starting Replay Negative Verification...")
    sys.path.append(os.getcwd())
    
    # 1. Execution (Firewall) in REPLAY mode
    print("  > Phase 2: Execution (Firewall Replay Check)...")
    from tests.prove_firewall_blocks_undocumented_side_effects import Firewall, load_json as load_json_fw
    fw_policy = load_json_fw("contracts/execution/firewall_policy.json")
    registry = [{"handler_id": "call_handler", "side_effects": [{"type": "EXTERNAL_CALL"}]}]
    fw = Firewall(fw_policy, registry)
    
    # Attempt EXTERNAL_CALL in REPLAY mode
    # Policy says REPLAY blocks "*"
    perm = fw.check_permission("REPLAY", "call_handler", "EXTERNAL_CALL")
    
    if perm != "BLOCKED_BY_MODE_REPLAY":
         print(f"    [FAIL] Expected BLOCKED_BY_MODE_REPLAY, got {perm}")
         sys.exit(1)
         
    print("    [PASS] Replay Mode Blocked Side Effect.")
    print("\n[SUCCESS] Replay Negative Scenario Proven.")

def main():
    try:
        test_replay_negative()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
