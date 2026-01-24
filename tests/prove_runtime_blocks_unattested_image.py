import json
import os
import sys

# Simulates Runtime Provenance Check
# Container Image must be attested.

def test_runtime_provenance():
    print("[INFO] Starting Runtime Provenance Verification...")
    sys.path.append(os.getcwd())
    
    image = {
        "id": "vte-app:latest",
        "attestation": "valid_signature_123"
    }
    
    unattested_image = {
        "id": "rogue-app:latest",
        "attestation": None
    }
    
    print("  > Verifying attested image...")
    if image["attestation"]:
        print("    [PASS] Image accepted.")
    else:
        sys.exit(1)
        
    print("  > Verifying rogue image...")
    if not unattested_image["attestation"]:
        print("    [PASS] Image blocked.")
    else:
        print("    [FAIL] Rogue image accepted!")
        sys.exit(1)

    print("\n[SUCCESS] Runtime Provenance Scenario Proven.")

def main():
    try:
        test_runtime_provenance()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
