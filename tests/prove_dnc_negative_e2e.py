import json
import os
import sys

# Simulates a flow blocked by DNC

def test_dnc_negative():
    print("[INFO] Starting DNC Negative Verification...")
    sys.path.append(os.getcwd())
    
    # 1. Policy Check (Compliance/Ops)
    print("  > Phase 1.27: Policy Check (Ensuring DNC Blocks)...")
    from tests.prove_policy_engine_blocks_dnc import PolicyEngine, load_json as load_json_policy
    defs = load_json_policy("contracts/compliance/policy_engine_definitions.json")
    engine = PolicyEngine(defs)
    
    # Use real policy which has DNC_GLOBAL enabled
    res = engine.check_access({"region": "NY", "current_hour": 10})
    
    if res != "BLOCKED_DNC":
        print(f"    [FAIL] Expected BLOCKED_DNC, got {res}")
        sys.exit(1)
        
    print("    [PASS] Verification Blocked as expected.")
    print("\n[SUCCESS] DNC Negative Scenario Proven.")

def main():
    try:
        test_dnc_negative()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
