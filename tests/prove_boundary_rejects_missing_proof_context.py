import sys
from spine.vte.core.integrity_verifier import IntegrityVerifier

# Proof: Boundary Rejects Missing Proof Context
# This ensures that "Ghost Requests" (untraced/unattributed) cannot enter the system.

def prove_context_rejection():
    print("Testing Proof Context Enforcement...")
    verifier = IntegrityVerifier()
    
    # Case 1: Missing Trace ID
    no_trace_ctx = {
        "tenant_id": "tenant-123",
        "actor_assurance_level": "AAL2"
    }
    
    print("  Case 1: Context missing Trace ID...")
    if verifier.verify_proof_context(no_trace_ctx):
        print("  [FAIL] Verifier accepted context without Trace ID!")
        return False
    else:
        print("  [PASS] Verifier rejected context without Trace ID.")

    return True

if __name__ == "__main__":
    if prove_context_rejection():
        sys.exit(0)
    else:
        sys.exit(1)
