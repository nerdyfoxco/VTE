import json
import os
import sys

# Contract paths
FIREWALL_POLICY = "contracts/execution/firewall_policy.json"
REGISTRY_SCHEMA = "contracts/execution/side_effect_registry_schema.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class Firewall:
    def __init__(self, policy, registry_data):
        self.policy = policy
        # Simplify registry lookup: map handler_id -> list of allowed side effects
        self.registry = {item['handler_id']: item['side_effects'] for item in registry_data}
        
    def check_permission(self, mode, handler_id, requested_effect_type):
        # 1. Check Registry
        if handler_id not in self.registry:
            return "BLOCKED_UNREGISTERED_HANDLER"
            
        allowed_effects = self.registry[handler_id]
        if not any(e['type'] == requested_effect_type for e in allowed_effects):
            return "BLOCKED_UNDOCUMENTED_SIDE_EFFECT"
            
        # 2. Check Policy (Mode)
        mode_rules = next((r for r in self.policy['rules'] if r['mode'] == mode), None)
        if not mode_rules:
            return "BLOCKED_UNKNOWN_MODE"
            
        # Deny list first (if present)
        if "block" in mode_rules:
             if "*" in mode_rules['block'] or requested_effect_type in mode_rules['block']:
                 return f"BLOCKED_BY_MODE_{mode}"
                 
        # Allow list
        if "allow" in mode_rules:
             if "*" in mode_rules['allow'] or requested_effect_type in mode_rules['allow']:
                 return "ALLOWED"
                 
        return "BLOCKED_DEFAULT"

def test_firewall_logic():
    print("[INFO] Loading Contracts...")
    policy = load_json(FIREWALL_POLICY)
    # Mock registry data conforming to schema
    registry = [
        {
            "handler_id": "handler_1",
            "side_effects": [
                {"type": "DB_READ"},
                {"type": "EXTERNAL_CALL"}
            ]
        }
    ]
    
    fw = Firewall(policy, registry)
    
    # 1. Registered + Safe Mode (LIVE) -> ALLOWED
    # LIVE allows * if registered
    res = fw.check_permission("LIVE", "handler_1", "EXTERNAL_CALL")
    if res != "ALLOWED":
        print(f"[FAIL] Expected ALLOWED for LIVE/Registered, got {res}")
        sys.exit(1)
    print("[PASS] LIVE mode allows registered side effect.")
    
    # 2. Registered + Unsafe Mode (SHADOW) -> BLOCKED
    # SHADOW blocks EXTERNAL_CALL
    res = fw.check_permission("SHADOW", "handler_1", "EXTERNAL_CALL")
    if res != "BLOCKED_BY_MODE_SHADOW":
        print(f"[FAIL] Expected BLOCKED_BY_MODE_SHADOW, got {res}")
        sys.exit(1)
    print("[PASS] SHADOW mode blocks unsafe side effect.")
    
    # 3. Registered + Safe Effect in SHADOW -> ALLOWED
    # SHADOW allows DB_READ
    res = fw.check_permission("SHADOW", "handler_1", "DB_READ")
    if res != "ALLOWED":
        print(f"[FAIL] Expected ALLOWED for SHADOW/DB_READ, got {res}")
        sys.exit(1)
    print("[PASS] SHADOW mode allows safe side effect.")
    
    # 4. Unregistered Side Effect -> BLOCKED
    # handler_1 does not have EMAIL_SEND
    res = fw.check_permission("LIVE", "handler_1", "EMAIL_SEND")
    if res != "BLOCKED_UNDOCUMENTED_SIDE_EFFECT":
        print(f"[FAIL] Expected BLOCKED_UNDOCUMENTED_SIDE_EFFECT, got {res}")
        sys.exit(1)
    print("[PASS] Undocumented side effect blocked.")

def main():
    try:
        test_firewall_logic()
        print("\n[SUCCESS] Firewall Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
