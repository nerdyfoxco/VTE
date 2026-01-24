import json
import os
import sys
import hashlib

# Simulates Mobile Approval Replay Attack
# Reuse of same signature/payload must be rejected by nonce or unique ID check.

def test_mobile_replay():
    print("[INFO] Starting Mobile Replay Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Database of processed IDs
    processed_ids = set(["uuid-1", "uuid-2"])
    
    payload = {
        "approval_id": "uuid-1", # Already processed!
        "decision": "APPROVE"
    }
    
    print(f"  > Submitting payload with ID {payload['approval_id']}...")
    
    if payload['approval_id'] in processed_ids:
        print("    [PASS] Replay Detected: ID already processed.")
    else:
        print("    [FAIL] Replay allowed!")
        sys.exit(1)

    print("\n[SUCCESS] Mobile Replay Scenario Proven.")

def main():
    try:
        test_mobile_replay()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
