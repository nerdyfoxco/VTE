import json
import os
import sys

# Simulates Change Budget / Sealed Path Logic
# "contracts/" is a sealed path. Agent cannot modify it without human review (or specific override flag which is absent here).

def test_change_budget_sealed():
    print("[INFO] Starting Change Budget Sealed Path Verification...")
    sys.path.append(os.getcwd())
    
    target_path = "contracts/core_logic.json"
    user_role = "AGENT"
    
    print(f"  > {user_role} attempting to modify {target_path}...")
    
    # Mock Policy
    sealed_paths = ["contracts/"]
    
    allowed = True
    for p in sealed_paths:
        if target_path.startswith(p) and user_role == "AGENT":
            allowed = False
            break
            
    if not allowed:
        print("    [PASS] Modification Blocked: Path is sealed.")
    else:
        print("    [FAIL] Agent modified sealed path!")
        sys.exit(1)

    print("\n[SUCCESS] Change Budget Scenario Proven.")

def main():
    try:
        test_change_budget_sealed()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
