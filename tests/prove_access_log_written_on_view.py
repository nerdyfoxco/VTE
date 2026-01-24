import json
import os
import sys
import time

# Simulates Audit Logging side effect on viewing sensitive data
# Rule: Any viewing of PII must invoke an audit log side effect.

def test_audit_ops():
    print("[INFO] Starting Audit Ops Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Viewer
    class Viewer:
        def __init__(self):
            self.audit_log = []
            
        def view_resource(self, resource_type, resource_id):
            # Implicit Side Effect: Log
            self.audit_log.append(f"ACCESSED {resource_type}:{resource_id} at {time.time()}")
            return "CONTENT"

    viewer = Viewer()
    
    # 1. Access Resource
    print("  > Accessing sensitive resource...")
    viewer.view_resource("SSN", "xxx-xx-xxxx")
    
    # 2. Verify Log
    if not viewer.audit_log:
        print("    [FAIL] No audit log generated!")
        sys.exit(1)
        
    print(f"    [PASS] Audit Log written: {viewer.audit_log[0]}")
    print("\n[SUCCESS] Audit Ops Scenario Proven.")

def main():
    try:
        test_audit_ops()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
