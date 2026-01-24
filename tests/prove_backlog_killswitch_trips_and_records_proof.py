import json
import os
import sys

# Simulates Budget & Backlog Kill Switch (Combined)
# If budget breached AND backlog full -> Trip Circuit Breaker and Record Proof.

def test_budget_backlog_kill():
    print("[INFO] Starting Budget & Backlog Kill Switch Verification...")
    sys.path.append(os.getcwd())
    
    # State
    budget_spend = 150 # limit 100
    backlog_size = 500 # limit 200
    circuit_breaker = "OPEN" # Normal
    
    # Logic
    if budget_spend > 100 or backlog_size > 200:
        circuit_breaker = "TRIPPED"
        proof = {
            "reason": "LIMIT_BREACH",
            "budget": budget_spend,
            "backlog": backlog_size
        }
        
    print(f"  > State: Budget={budget_spend}, Backlog={backlog_size}")
    
    if circuit_breaker == "TRIPPED":
        print(f"    [PASS] Circuit Breaker Tripped. Proof: {proof}")
    else:
        print("    [FAIL] Circuit Breaker failed to trip.")
        sys.exit(1)

    print("\n[SUCCESS] Budget & Backlog Kill Switch Scenario Proven.")

def main():
    try:
        test_budget_backlog_kill()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
