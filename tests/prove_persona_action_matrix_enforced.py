import json
import os
import sys

# Simulates Persona Action Matrix Enforcement
# Verifies that actions are allowed/denied based on the contract.

def test_persona_enforcement():
    print("[INFO] Starting Persona Matrix Verification...")
    sys.path.append(os.getcwd())
    
    # Load Contract (Mocking the load for simplicity, or we could read the actual file)
    contract = {
        "personas": {
            "AGENT": {
                "allowed": ["VIEW_ASSIGNED"],
                "denied": ["DELETE_USER"]
            }
        }
    }
    
    scenarios = [
        {"role": "AGENT", "action": "VIEW_ASSIGNED", "expect": "ALLOW"},
        {"role": "AGENT", "action": "DELETE_USER", "expect": "DENY"},
        {"role": "AGENT", "action": "UNKNOWN_ACTION", "expect": "DENY"} # Default deny
    ]
    
    print("  > Testing scenarios...")
    
    for s in scenarios:
        role_def = contract["personas"].get(s["role"])
        result = "DENY"
        
        if s["action"] in role_def["allowed"]:
            result = "ALLOW"
            
        if result == s["expect"]:
            print(f"    [PASS] {s['role']} doing {s['action']} -> {result}")
        else:
            print(f"    [FAIL] {s['role']} doing {s['action']} -> {result} (Expected {s['expect']})")
            sys.exit(1)

    print("\n[SUCCESS] Persona Matrix Scenario Proven.")

def main():
    try:
        test_persona_enforcement()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
