import json
import os
import sys

# Simulates Invalid Mobile Signature using the existing Signing Canary logic

def test_approval_sig_fail():
    print("[INFO] Starting Approval Sig Fail Verification...")
    sys.path.append(os.getcwd())
    
    # Reuse the mock signer/verifier from Phase 3
    # We'll just re-implement the fail case explicitly as a dedicated canary
    from tests.prove_mobile_signing_validity import SignatureVerifier
    
    print("  > Phase 3: Mobile Approval...")
    verifier = SignatureVerifier("secret_key_123")
    payload = {
        "approval_id": "uuid-1", 
        "decision": "APPROVE"
    }
    
    # Case 1: Tampered Data
    bad_payload = payload.copy()
    bad_payload['decision'] = "REJECT"
    # Valid sig for ORIGINAL payload
    # In a real scenario, we'd generate a sig for 'payload', then check 'bad_payload'.
    # For this mock, we can just pass a dummy sig and assert failure, 
    # OR replicate the signing logic locally.
    # Let's import SecureSigner too to be precise.
    from tests.prove_mobile_signing_validity import SecureSigner
    signer = SecureSigner("secret_key_123")
    valid_sig = signer.sign(payload)
    
    if verifier.verify(bad_payload, valid_sig):
        print("    [FAIL] Tampered payload accepted!")
        sys.exit(1)
    print("    [PASS] Tampered payload rejected.")

    # Case 2: Invalid Key
    bad_verifier = SignatureVerifier("WRONG_KEY")
    if bad_verifier.verify(payload, valid_sig):
        print("    [FAIL] Wrong key accepted signature!")
        sys.exit(1)
    print("    [PASS] Wrong key rejected signature.")
    
    print("\n[SUCCESS] Approval Sig Negative Scenario Proven.")

def main():
    try:
        test_approval_sig_fail()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
