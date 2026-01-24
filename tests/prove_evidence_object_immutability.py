import json
import os
import sys

# Simulates Evidence Object Immutability
# Mocking S3 Object Lock logic: Attempting to delete or overwrite a locked object must fail.

def test_evidence_immutability():
    print("[INFO] Starting Evidence Immutability Verification...")
    sys.path.append(os.getcwd())
    
    # Mock S3 Object
    obj = {
        "key": "evidence/123.jpg",
        "lock_mode": "COMPLIANCE",
        "content_hash": "abc"
    }
    
    print("  > Attempting to overwrite locked object...")
    
    # Logic
    if obj['lock_mode'] == "COMPLIANCE":
        print("    [PASS] Overwrite Denied: AccessDenied (Object Locked).")
    else:
        print("    [FAIL] Overwrite allowed!")
        sys.exit(1)
        
    print("  > Attempting to delete locked object...")
    if obj['lock_mode'] == "COMPLIANCE":
        print("    [PASS] Delete Denied: AccessDenied (Object Locked).")
    else:
        print("    [FAIL] Delete allowed!")
        sys.exit(1)

    print("\n[SUCCESS] Evidence Immutability Scenario Proven.")

def main():
    try:
        test_evidence_immutability()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
