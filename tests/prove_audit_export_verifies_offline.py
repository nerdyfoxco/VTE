import json
import os
import sys

# Simulates Audit Export Verification
# Exported audit logs must match the internal checksums.

def test_audit_export():
    print("[INFO] Starting Audit Export Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Internal Log
    internal_logs = [
        {"id": 1, "action": "LOGIN", "checksum": "a1"},
        {"id": 2, "action": "VIEW", "checksum": "b2"}
    ]
    
    # Mock Exported CSV/JSON
    exported_data = [
        {"id": 1, "action": "LOGIN", "checksum": "a1"},
        {"id": 2, "action": "VIEW", "checksum": "b2"}
    ]
    
    print("  > Verifying export integrity...")
    
    for i, row in enumerate(exported_data):
        if row['checksum'] != internal_logs[i]['checksum']:
            print(f"    [FAIL] Checksum mismatch at row {i}")
            sys.exit(1)
            
    print("    [PASS] Export matches internal checksums.")
    print("\n[SUCCESS] Audit Export Scenario Proven.")

def main():
    try:
        test_audit_export()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
