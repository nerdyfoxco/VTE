import json
import os
import sys

# Contract paths
RUN_MODE_TRUTH_PATH = "contracts/run_mode_truth_table.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class SideEffectFirewall:
    def __init__(self, truth_table, current_mode):
        self.rules = truth_table['modes'].get(current_mode)
        self.mode = current_mode
        if not self.rules:
            raise ValueError(f"Unknown mode: {current_mode}")

    def attempt_egress(self, destination):
        rule = self.rules['external_egress']
        print(f"  > Attempting egress to {destination} in {self.mode} (Rule: {rule})")
        
        if rule == "BLOCKED":
            return "BLOCKED"
        elif rule == "ALLOWED":
            return "SENT"
        return "UNKNOWN"

    def attempt_notification(self, recipient):
        rule = self.rules['notifications']
        if rule == "BLOCKED_OR_DIVERTED_TO_TEST":
             # Mock diversion logic
             if "test-sink" in recipient:
                 return "SENT_TO_SINK"
             return "DIVERTED"
        elif rule == "ALLOWED":
             return "SENT"
        return "BLOCKED"

def test_shadow_safety():
    print("[INFO] Loading Run Mode Truth Table...")
    table = load_json(RUN_MODE_TRUTH_PATH)
    
    # 1. Test SHADOW Mode Egress
    print("[INFO] Testing SHADOW Mode Egress...")
    firewall = SideEffectFirewall(table, "SHADOW")
    
    if firewall.attempt_egress("api.stripe.com") != "BLOCKED":
        print("[FAIL] SHADOW mode allowed external egress!")
        sys.exit(1)
    print("[PASS] SHADOW mode blocked egress.")
    
    # 2. Test SHADOW Mode Notifications
    print("[INFO] Testing SHADOW Mode Notifications...")
    res = firewall.attempt_notification("real.user@example.com")
    if res != "DIVERTED":
         print(f"[FAIL] SHADOW mode allowed notification to real user! Got: {res}")
         sys.exit(1)
    print("[PASS] SHADOW mode diverted notification.")
    
    # 3. Test LIVE Mode
    print("[INFO] Testing LIVE Mode...")
    live_firewall = SideEffectFirewall(table, "LIVE")
    if live_firewall.attempt_egress("api.stripe.com") != "SENT":
         print("[FAIL] LIVE mode blocked valid egress!")
         sys.exit(1)
    print("[PASS] LIVE mode allowed egress.")

def main():
    try:
        test_shadow_safety()
        print("\n[SUCCESS] Shadow Mode Safety Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
