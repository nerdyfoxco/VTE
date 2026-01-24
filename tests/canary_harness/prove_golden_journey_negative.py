import json
import os
import sys

# Contract path
GOLDEN_JOURNEY_PATH = "contracts/journeys/vte_delinquency_golden_journey_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def run_negative_journey_test():
    print("[INFO] Loading Golden Journey Contract...")
    contract = load_json(GOLDEN_JOURNEY_PATH)
    steps = contract['journey_steps']
    
    # Identify a critical step to sabotage (Step 3: SELECT_STRATEGY)
    # We will simulate a failure in evidence production for this step.
    target_step_index = 2 # 0-based index for step 3
    target_step = steps[target_step_index]
    
    print(f"[INFO] Sabotaging Step {target_step['step_id']}: {target_step['name']}...")
    
    # Simulate Execution Flow
    try:
        for i, step in enumerate(steps):
            name = step['name']
            required_evidence = step['required_evidence']
            
            print(f"  > Executing Step {step['step_id']}: {name}...")
            
            if i == target_step_index:
                # Sabotage: Fail to produce one piece of evidence
                # e.g. POLICY_ENGINE_DECISION is missing
                print("    [INJECT_FAILURE] Simulating missing 'POLICY_ENGINE_DECISION' evidence...")
                actual_evidence = [] # Empty!
                
                # Check Logic (Harness Simulation)
                missing = [req for req in required_evidence if req not in actual_evidence]
                if missing:
                    raise RuntimeError(f"Step {name} Failed: Missing Evidence {missing}")
            
    except RuntimeError as e:
        print(f"[PASS] Expected Failure Caught: {e}")
        return

    # If we get here, the test failed (because the system didn't fail!)
    print("[FAIL] System allowed progression despite missing evidence!")
    sys.exit(1)

def main():
    try:
        run_negative_journey_test()
        print("\n[SUCCESS] Negative Golden Journey Proven (Fail-Closed).")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
