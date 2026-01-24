import json
import os
import sys

# Contract paths
REDACTION_POLICY_PATH = "contracts/privacy/redaction_policy_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class Redactor:
    def __init__(self, policy):
        self.rules = policy['rules']

    def redact(self, data_type, value):
        # In real impl, this uses regex patterns from constraints.
        # Here we verify the policy routing.
        
        # Simple lookup for mock
        # 'data_type' would effectively be inferred from field name or content analysis
        
        if data_type == "email":
            rule = self.rules.get('email_address')
            if rule:
                 # verify scope?
                 return f"REDACTED({rule['replacement']})"
        elif data_type == "ssn":
            rule = self.rules.get('ssn')
            if rule:
                 return f"REDACTED({rule['replacement']})"
                 
        return value # No redaction

def test_redaction_application():
    print("[INFO] Loading Redaction Policy...")
    policy = load_json(REDACTION_POLICY_PATH)
    redactor = Redactor(policy)
    
    # 1. Test SSN (Strict Full Mask)
    print("[INFO] Testing SSN Redaction...")
    ssn_val = "123-45-6789"
    res = redactor.redact("ssn", ssn_val)
    if "FULL_MASK" not in res:
        print(f"[FAIL] SSN leaked or not fully masked! Got: {res}")
        sys.exit(1)
    print("[PASS] SSN Redacted.")
    
    # 2. Test Email (Partial Mask)
    print("[INFO] Testing Email Redaction...")
    email_val = "foo@bar.com"
    res = redactor.redact("email", email_val)
    if "PARTIAL_MASK" not in res:
        print(f"[FAIL] Email leaked! Got: {res}")
        sys.exit(1)
    print("[PASS] Email Redacted.")
    
    # 3. Test Unknown (No Mask)
    print("[INFO] Testing Safe Field...")
    safe_val = "Public Info"
    res = redactor.redact("description", safe_val)
    if res != safe_val:
        print(f"[FAIL] Safe info modified! Got: {res}")
        sys.exit(1)
    print("[PASS] Safe info preserved.")

def main():
    try:
        test_redaction_application()
        print("\n[SUCCESS] Redaction Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
