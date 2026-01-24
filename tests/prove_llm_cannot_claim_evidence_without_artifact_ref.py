import json
import os
import sys

# Simulates LLM Evidence Claim
# LLM cannot say "I verified X" without linking to Artifact ID of X.

def test_llm_claim_evidence():
    print("[INFO] Starting LLM Evidence Claim Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Claim Validator
    def validate_claim(claim_text, artifacts):
        if "verified" in claim_text and not artifacts:
            return "BLOCKED_CLAIM_WITHOUT_EVIDENCE"
        return "ACCEPTED"
        
    claim = "I verified the document."
    artifacts = [] # Empty!
    
    print(f"  > LLM claiming: '{claim}' with artifacts: {artifacts}")
    
    res = validate_claim(claim, artifacts)
    
    if res == "BLOCKED_CLAIM_WITHOUT_EVIDENCE":
        print("    [PASS] Unsubstantiated claim blocked.")
    else:
        print(f"    [FAIL] Claim accepted without evidence: {res}")
        sys.exit(1)

    print("\n[SUCCESS] LLM Evidence Claim Scenario Proven.")

def main():
    try:
        test_llm_claim_evidence()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
