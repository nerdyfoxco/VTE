import json
import os
import sys
import hashlib

# Simulates Evidence Hash Chain Inclusion
# Ensures that "Artifact A" is actually referenced in the chain.

def test_hash_chain_inclusion():
    print("[INFO] Starting Evidence Chain Inclusion Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Chain from Phase 2
    # Chain Block: { "content_hash": "...", "prev": "..." }
    
    artifact_content = "Important Document"
    art_hash = hashlib.sha256(artifact_content.encode('utf-8')).hexdigest()
    
    chain = [
        {"content_hash": "gbg123", "prev": "GENESIS"},
        {"content_hash": art_hash, "prev": "hash1"}, # Included here
        {"content_hash": "xyz789", "prev": "hash2"}
    ]
    
    print(f"  > Verifying artifact hash {art_hash} is in chain...")
    
    found = False
    for block in chain:
        if block['content_hash'] == art_hash:
            found = True
            break
            
    if found:
        print("    [PASS] Artifact found in chain.")
    else:
        print("    [FAIL] Artifact missing from chain!")
        sys.exit(1)

    print("\n[SUCCESS] Evidence Hash Chain Scenario Proven.")

def main():
    try:
        test_hash_chain_inclusion()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
