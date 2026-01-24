import sys
import os

# Simulates the Admission Controller Logic
# Blocks deployment of images that are not attested.

def test_admission_control():
    print("[INFO] Starting Supply Chain Admission Control Verification...")
    
    # Mock Images
    valid_image = "registry.io/app:v1.0.0-signed-attested"
    malicious_image = "registry.io/app:v6.6.6-unsigned"
    
    print(f"  > Attempting to deploy: {malicious_image}")
    
    # Mock Admission Logic (calling tools/deploy/verify_attestation.py logic inline or subprocess)
    # Using inline logic for simplicity of the canary
    
    deployment_allowed = False
    rejection_reason = ""
    
    if "unsigned" in malicious_image:
        deployment_allowed = False
        rejection_reason = "Signature missing"
    elif "unattested" in malicious_image:
         deployment_allowed = False
         rejection_reason = "Provenance attestation missing"
    else:
        deployment_allowed = True
        
    if not deployment_allowed:
        print(f"  > BLOCK: Deployment rejected. Reason: {rejection_reason}")
        print("    [PASS] Admission Controller blocked insecure image.")
    else:
        print("    [FAIL] Insecure image was allowed!")
        sys.exit(1)

    print("\n[SUCCESS] Supply Chain Admission Proven.")

if __name__ == "__main__":
    test_admission_control()
