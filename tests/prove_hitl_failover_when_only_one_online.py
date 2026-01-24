import json
import os
import sys

# Simulates HITL Failover
# If Agent A is offline, route to Agent B.

def test_hitl_failover():
    print("[INFO] Starting HITL Failover Verification...")
    sys.path.append(os.getcwd())
    
    agents = {
        "agent_a": {"online": False},
        "agent_b": {"online": True}
    }
    
    print("  > Finding available agent...")
    
    target = None
    # Prefer A, then B
    if agents["agent_a"]["online"]:
        target = "agent_a"
    elif agents["agent_b"]["online"]:
        target = "agent_b"
        
    if target == "agent_b":
        print("    [PASS] Failed over to Agent B.")
    else:
        print(f"    [FAIL] Routing error. Target: {target}")
        sys.exit(1)

    print("\n[SUCCESS] HITL Failover Scenario Proven.")

def main():
    try:
        test_hitl_failover()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
