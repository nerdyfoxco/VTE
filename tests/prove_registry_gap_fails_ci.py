import json
import os
import sys

# Simulates Registry Gap (Side effect in code not in registry)
# This is essentially the same as "Drift" but framed as a CI check failure.

def test_registry_gap_fails_ci():
    print("[INFO] Starting Registry Gap CI Verification...")
    sys.path.append(os.getcwd())
    
    print("  > Phase 2: Registry Gap Check...")
    from tests.prove_firewall_blocks_undocumented_side_effects import Firewall, load_json as load_json_fw
    fw_policy = load_json_fw("contracts/execution/firewall_policy.json")
    
    # Handler declares NO side effects
    registry = [{"handler_id": "clean_handler", "side_effects": []}]
    fw = Firewall(fw_policy, registry)
    
    # Code tries to do something
    perm = fw.check_permission("LIVE", "clean_handler", "LOGGING")
    
    # LIVE mode generally allows LOGGING if registered, or maybe block if specific?
    # Firewall policy: LIVE allows "*" IF REGISTERED.
    # Registry has handling for "clean_handler" but empty list.
    # So logical result: BLOCKED_UNDOCUMENTED_SIDE_EFFECT
    
    if perm != "BLOCKED_UNDOCUMENTED_SIDE_EFFECT":
         print(f"    [FAIL] Expected BLOCKED_UNDOCUMENTED_SIDE_EFFECT, got {perm}")
         sys.exit(1)
         
    print("    [PASS] Gap caught.")
    print("\n[SUCCESS] Registry Gap Negative Scenario Proven.")

def main():
    try:
        test_registry_gap_fails_ci()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
