import json
import os
import sys

# Simulates Queue Kill Switch
# Reuses SystemLayer logic from Phase 2, but specifically testing Queue PAUSE

def test_queue_kill_switch():
    print("[INFO] Starting Queue Kill Switch Verification...")
    sys.path.append(os.getcwd())
    
    print("  > Phase 2: Kill Switch (Queue Layer)...")
    from tests.prove_kill_switch_propagates_to_all_layers import SystemLayer, load_json as load_json_policy
    policy = load_json_policy("contracts/execution/kill_switch_policy.json")
    
    queue_layer = SystemLayer("QUEUE")
    
    # 1. Normal State
    if not queue_layer.active:
        print("    [FAIL] Queue should be active initially.")
        sys.exit(1)
        
    # 2. Trigger Signal
    signal = "GLOBAL_KILL_SIGNAL"
    action = queue_layer.check_signal(signal, policy)
    
    if action != "PAUSE_CONSUMPTION":
        print(f"    [FAIL] Expected PAUSE_CONSUMPTION, got {action}")
        sys.exit(1)
        
    if queue_layer.active:
        print("    [FAIL] Queue layer should be inactive (paused).")
        sys.exit(1)
        
    print("    [PASS] Queue Consumption Paused on Signal.")
    print("\n[SUCCESS] Queue Kill Switch Scenario Proven.")

def main():
    try:
        test_queue_kill_switch()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
