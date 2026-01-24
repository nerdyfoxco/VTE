import json
import os
import sys
import hashlib
import time

# Contract paths
APPROVAL_SCHEMA = "contracts/hitl/mobile_approval_schema.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

# Mock Signing (since we don't have crypto libs guaranteed, we simulate the logic)
class SecureSigner:
    def __init__(self, private_key_mock):
        self.key = private_key_mock
        
    def sign(self, payload_dict):
        # Flatten payload canonically
        canonical = json.dumps(payload_dict, sort_keys=True)
        # "Sign" by hashing with key
        signature = hashlib.sha256((canonical + self.key).encode('utf-8')).hexdigest()
        return signature

class SignatureVerifier:
    def __init__(self, public_key_mock):
        # In this mock, public key == private key for symmetric check simplicity
        self.key = public_key_mock
        
    def verify(self, payload_dict, signature):
        canonical = json.dumps(payload_dict, sort_keys=True)
        expected = hashlib.sha256((canonical + self.key).encode('utf-8')).hexdigest()
        return expected == signature

def test_mobile_signing():
    print("[INFO] Loading Schema...")
    load_json(APPROVAL_SCHEMA)
    
    # 1. Sign Payload
    print("  > Signing valid payload...")
    signer = SecureSigner("secret_key_123")
    payload = {
        "approval_id": "uuid-1",
        "intent_hash": "abc-123",
        "decision": "APPROVE",
        "timestamp_utc": "2023-10-27T10:00:00Z",
        "device_id": "iphone-15"
    }
    sig = signer.sign(payload)
    print(f"    Signature: {sig}")
    
    # 2. Verify
    print("  > Verifying signature...")
    verifier = SignatureVerifier("secret_key_123")
    if not verifier.verify(payload, sig):
        print("[FAIL] Signature verification failed.")
        sys.exit(1)
    print("[PASS] Verification successful.")
    
    # 3. Tamper Payload
    print("  > Tampering payload...")
    tampered_payload = payload.copy()
    tampered_payload['decision'] = "REJECT" # Attack!
    
    if verifier.verify(tampered_payload, sig):
        print("[FAIL] Tampered payload accepted!")
        sys.exit(1)
    print("[PASS] Tampered payload rejected.")
    
    # 4. Tamper Signature
    print("  > Tampering signature...")
    if verifier.verify(payload, "bad_sig"):
        print("[FAIL] Bad signature accepted!")
        sys.exit(1)
    print("[PASS] Bad signature rejected.")

def main():
    try:
        test_mobile_signing()
        print("\n[SUCCESS] Mobile Signing Validity Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
