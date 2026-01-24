import json
import os
import sys

# Simulates SHADOW Bypass Attempt
# SHADOW mode should block EXTERNAL_CALL.
# "Bypass" means trying to force it or ignoring the error.
# We verify the firewall holds even if we "really really want it".

def test_shadow_bypass_negative():
    print("[INFO] Starting SHADOW Bypass Negative Verification...")
    sys.path.append(os.getcwd())
    
    # 1. Execution (Firewall)
    print("  > Phase 2: Execution (Firewall SHADOW Check)...")
    from tests.prove_firewall_blocks_undocumented_side_effects import Firewall, load_json as load_json_fw
    fw_policy = load_json_fw("contracts/execution/firewall_policy.json")
    registry = [{"handler_id": "call_handler", "side_effects": [{"type": "EXTERNAL_CALL"}]}]
    fw = Firewall(fw_policy, registry)
    
    # Attempt EXTERNAL_CALL in SHADOW
    # Even if valid in REGISTRY, SHADOW overrides it.
    perm = fw.check_permission("SHADOW", "call_handler", "EXTERNAL_CALL")
    
    # SHADOW policy blocks EXTERNAL_CALL explicitly
    if perm != "BLOCKED_BY_MODE_SHADOW":
         print(f"    [FAIL] Expected BLOCKED_BY_MODE_SHADOW, got {perm}")
         sys.exit(1)
         
    print("    [PASS] SHADOW Mode Blocked Side Effect (No Bypass).")
    print("\n[SUCCESS] SHADOW Bypass Negative Scenario Proven.")

def main():
    try:
        test_shadow_bypass_negative()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
