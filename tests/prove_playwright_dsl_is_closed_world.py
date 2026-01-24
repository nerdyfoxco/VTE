import json
import os
import sys

# Contract paths
DSL_SCHEMA = "contracts/execution/playwright_dsl_schema.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class DSLValidator:
    def __init__(self, schema):
        self.allowed = {a['action']: a for a in schema['allowed_actions']}
        self.forbidden = schema['forbidden_patterns']
        
    def validate_step(self, step):
        # 1. Check Action allow-list
        if step['action'] not in self.allowed:
            return "BLOCKED_UNKNOWN_ACTION"
            
        # 2. Check Params against Forbidden patterns
        for key, val in step.get('args', {}).items():
            if isinstance(val, str):
                for pattern in self.forbidden:
                    if pattern in val:
                        return f"BLOCKED_FORBIDDEN_PATTERN: {pattern}"
                        
        return "ALLOWED"

def test_dsl_constraints():
    print("[INFO] Loading DSL Schema...")
    schema = load_json(DSL_SCHEMA)
    val = DSLValidator(schema)
    
    # 1. Valid Action
    print("  > Testing valid action...")
    res = val.validate_step({"action": "CLICK", "args": {"selector": "#btn"}})
    if res != "ALLOWED":
         print(f"[FAIL] Valid action rejected: {res}")
         sys.exit(1)
    print("[PASS] Valid action accepted.")
    
    # 2. Unknown Action
    print("  > Testing unknown action...")
    res = val.validate_step({"action": "DOWNLOAD_FILE", "args": {}})
    if res != "BLOCKED_UNKNOWN_ACTION":
         print(f"[FAIL] Expected BLOCKED_UNKNOWN_ACTION, got {res}")
         sys.exit(1)
    print("[PASS] Unknown action blocked.")
    
    # 3. Forbidden Pattern (Injection)
    print("  > Testing forbidden pattern...")
    res = val.validate_step({"action": "TYPE", "args": {"selector": "#input", "text": "eval(alert('xss'))"}})
    if "BLOCKED_FORBIDDEN_PATTERN" not in res:
         print(f"[FAIL] Should have blocked 'eval'. Got {res}")
         sys.exit(1)
    print("[PASS] Forbidden pattern blocked.")

def main():
    try:
        test_dsl_constraints()
        print("\n[SUCCESS] DSL Closed World Constraints Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
