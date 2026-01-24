import sys
import json

def verify_image(image_url):
    # Mock verifying an image signature
    if "unsigned" in image_url:
        return False, "Signature missing"
    if "unattested" in image_url:
        return False, "Provenance attestation missing"
    return True, "Verified"

def main():
    if len(sys.argv) < 2:
        print("Usage: verify_attestation.py <image>")
        sys.exit(1)
        
    image = sys.argv[1]
    valid, msg = verify_image(image)
    if valid:
        print(f"[PASS] {image}: {msg}")
    else:
        print(f"[FAIL] {image}: {msg}")
        sys.exit(1)

if __name__ == "__main__":
    main()
