import sys
from spine.vte.core.integrity_verifier import IntegrityVerifier

# Proof: Unsigned Evidence Rejected

def prove_unsigned_rejection():
    print("Testing Evidence Signature Enforcement...")
    verifier = IntegrityVerifier()
    
    # Case 1: No Signature
    unsigned_bundle = {
        "data": "sensitive_decision_ctx",
        "timestamp": "2026-01-23T12:00:00Z"
    }
    
    print("  Case 1: Submitting Unsigned Bundle...")
    if verifier.verify_evidence_integrity(unsigned_bundle):
        print("  [FAIL] Verifier accepted unsigned evidence!")
        return False
    else:
        print("  [PASS] Verifier rejected unsigned evidence.")

    # Case 2: Invalid Signature
    bad_sig_bundle = {
        "data": "sensitive_decision_ctx",
        "timestamp": "2026-01-23T12:00:00Z",
        "signature": "INVALID_SIG"
    }
    
    print("  Case 2: Submitting Invalid Signature...")
    if verifier.verify_evidence_integrity(bad_sig_bundle):
        print("  [FAIL] Verifier accepted invalid signature!")
        return False
    else:
        print("  [PASS] Verifier rejected invalid signature.")

    return True

if __name__ == "__main__":
    if prove_unsigned_rejection():
        sys.exit(0)
    else:
        sys.exit(1)
