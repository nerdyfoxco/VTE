import json
import os
import sys

# Contract paths
KILL_SWITCH_POLICY = "contracts/execution/kill_switch_policy.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class SystemLayer:
    def __init__(self, name):
        self.name = name
        self.active = True
        
    def check_signal(self, signal, policy):
        # Find rule for this layer
        rule = next((r for r in policy['layers'] if r['layer'] == self.name), None)
        if rule and rule['trigger'] == signal:
            print(f"  > Layer {self.name} received {signal}. Executing {rule['action']}...")
            self.active = False
            return rule['action']
        return "NO_ACTION"

def test_kill_switch():
    print("[INFO] Loading Policy...")
    policy = load_json(KILL_SWITCH_POLICY)
    
    layers = [
        SystemLayer("FIREWALL"),
        SystemLayer("RUNNER"),
        SystemLayer("QUEUE"),
        SystemLayer("CONNECTORS")
    ]
    
    # 1. Trigger Global Kill
    print("  > Triggering GLOBAL_KILL_SIGNAL...")
    signal = "GLOBAL_KILL_SIGNAL"
    
    for layer in layers:
        layer.check_signal(signal, policy)
        
    # 2. Verify all Layers Stopped
    if any(l.active for l in layers):
        print(f"[FAIL] Some layers are still active: {[l.name for l in layers if l.active]}")
        sys.exit(1)
        
    print("[PASS] All layers responded to kill signal.")

def main():
    try:
        test_kill_switch()
        print("\n[SUCCESS] Kill Switch Propagation Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
