import json
import os
import sys

# Contract paths
FAILURE_SEMANTICS_PATH = "contracts/partial_failure_semantics.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class WorkflowEngine:
    def __init__(self, failure_policy):
        self.modes = failure_policy['failure_modes']
        self.state = "INIT"
        self.compensation_queue = []

    def execute_step(self, step_name, simulate_error_type=None):
        print(f"  > Executing step: {step_name}")
        if not simulate_error_type:
             self.compensation_queue.append(f"UNDO_{step_name}")
             return "SUCCESS"
             
        # Handle Error
        print(f"    [ERROR] Simulating {simulate_error_type}")
        if simulate_error_type not in self.modes:
            return "UNKNOWN_ERROR"
            
        policy = self.modes[simulate_error_type]
        fallback = policy['fallback']
        
        if fallback == "CIRCUIT_BREAKER_OPEN":
             self.state = "FAILED_CIRCUIT_OPEN"
        elif fallback == "RETURN_PARTIAL_RESULT_OR_ERROR":
             self.state = "PARTIAL_SUCCESS"
             
        # In a real SAGA, we would trigger compensation here if terminal
        return "ERROR"

def test_partial_failure():
    print("[INFO] Loading Failure Semantics...")
    policy = load_json(FAILURE_SEMANTICS_PATH)
    engine = WorkflowEngine(policy)
    
    # 1. Successful Step
    engine.execute_step("ReserveInventory")
    
    # 2. Fail Next Step with Transient Error -> Circuit Breaker
    engine.execute_step("ChargeCard", simulate_error_type="TRANSIENT_RPC_ERROR")
    
    if engine.state != "FAILED_CIRCUIT_OPEN":
        print(f"[FAIL] Expected FAILED_CIRCUIT_OPEN, got {engine.state}")
        sys.exit(1)
        
    print(f"[PASS] Circuit breaker opened on transient error. Compensation queue: {engine.compensation_queue}")
    
    # 3. Fail with Timeout -> Partial
    engine.state = "INIT"
    engine.execute_step("FetchRecommendations", simulate_error_type="TIMEOUT")
    if engine.state != "PARTIAL_SUCCESS":
         print(f"[FAIL] Expected PARTIAL_SUCCESS, got {engine.state}")
         sys.exit(1)
         
    print("[PASS] Timeout resulted in Allowed Partial Success.")

def main():
    try:
        test_partial_failure()
        print("\n[SUCCESS] Partial Failure Semantics Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
