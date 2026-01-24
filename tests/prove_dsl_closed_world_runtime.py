import json
import os
import sys

# Simulates DSL Closed World Failure (Runtime Eval Injection)
# We re-use logic from Phase 2 but specifically test the "eval" injection path again 
# to confirm it fails.

def test_dsl_closed_world_runtime():
    print("[INFO] Starting DSL Closed World Runtime Verification...")
    sys.path.append(os.getcwd())
    
    print("  > Phase 2: DSL Validation...")
    from tests.prove_playwright_dsl_is_closed_world import DSLValidator, load_json as load_json_dsl
    schema = load_json_dsl("contracts/execution/playwright_dsl_schema.json")
    val = DSLValidator(schema)
    
    # Attempt Eval Injection
    # Action 'TYPE' is allowed, but 'eval()' in text arg is forbidden
    step = {
        "action": "TYPE", 
        "args": {
            "selector": "#search", 
            "text": "'); eval('rm -rf /'); //"
        }
    }
    
    res = val.validate_step(step)
    
    if "BLOCKED_FORBIDDEN_PATTERN" not in res:
         print(f"    [FAIL] Expected BLOCKED_FORBIDDEN_PATTERN, got {res}")
         sys.exit(1)
         
    print("    [PASS] Eval Injection Blocked.")
    print("\n[SUCCESS] DSL Closed World Negative Scenario Proven.")

def main():
    try:
        test_dsl_closed_world_runtime()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
