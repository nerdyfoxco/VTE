import sys

# Proof: Unapproved Model Promotion Blocked
# Ensures that experimental or quarantined models CANNOT take real actions.

class GovernanceGate:
    def __init__(self):
        self.model_registry = {
            "model_A": "LIVE_PRIMARY",
            "model_B": "SHADOW_MODE",
            "model_C": "QUARANTINE"
        }
    
    def authorize_execution(self, model_id):
        status = self.model_registry.get(model_id, "UNKNOWN")
        if status != "LIVE_PRIMARY":
             raise PermissionError(f"Model {model_id} is {status}. Execution Denied.")
        return True

def prove_promotion_gate():
    print("Testing Model Promotion Gate...")
    gate = GovernanceGate()
    
    # 1. Test Live Model
    try:
        gate.authorize_execution("model_A")
        print("  [PASS] Live Model A authorized.")
    except Exception as e:
        print(f"  [FAIL] Live Model A rejected: {e}")
        return False
        
    # 2. Test Shadow Model
    try:
        gate.authorize_execution("model_B")
        print("  [FAIL] Shadow Model B allowed to execute!")
        return False
    except PermissionError:
        print("  [PASS] Shadow Model B blocked (Safety Mode).")
        
    # 3. Test Quarantine Model
    try:
        gate.authorize_execution("model_C")
        print("  [FAIL] Quarantined Model C allowed to execute!")
        return False
    except PermissionError:
        print("  [PASS] Quarantined Model C blocked.")
        
    return True

if __name__ == "__main__":
    if prove_promotion_gate():
        sys.exit(0)
    else:
        sys.exit(1)
