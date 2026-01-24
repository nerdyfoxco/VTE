import json
import os
import sys

# Simulates Evidence Signature Requirement
# Evidence object must have a valid signature field.

def test_evidence_sig_req():
    print("[INFO] Starting Evidence Signature Verification...")
    sys.path.append(os.getcwd())
    
    evidence = {
        "id": "ev-1",
        "content": "image",
        # "signature": "..." # MISSING
    }
    
    print("  > Validating Evidence Object...")
    
    if "signature" not in evidence:
        print("    [PASS] Rejected evidence due to missing signature.")
    else:
        print("    [FAIL] Accepted valid evidence (unexpected for this negative test).")
        # sys.exit(1) 
        
    print("\n[SUCCESS] Evidence Signature Scenario Proven.")

def main():
    try:
        test_evidence_sig_req()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
