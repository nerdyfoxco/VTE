import json
import os
import sys
import hashlib

# Contract paths
METADATA_SCHEMA = "contracts/execution/evidence_metadata_schema.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class EvidenceChain:
    def __init__(self):
        self.chain = []
        
    def add_evidence(self, content):
        prev_hash = self.chain[-1]['this_hash'] if self.chain else "GENESIS"
        
        # Hash content first
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Create metadata block
        metadata = {
            "content_hash": content_hash,
            "previous_evidence_hash": prev_hash,
            "nonce": len(self.chain) # Simple nonce
        }
        
        # Hash the metadata to create the link ID
        meta_str = json.dumps(metadata, sort_keys=True)
        this_hash = hashlib.sha256(meta_str.encode('utf-8')).hexdigest()
        
        metadata['this_hash'] = this_hash
        self.chain.append(metadata)
        return this_hash
        
    def verify(self):
        prev_hash = "GENESIS"
        for i, block in enumerate(self.chain):
            if block['previous_evidence_hash'] != prev_hash:
                return False, i
            
            # Recompute this_hash
            # We must remove 'this_hash' from dict to verify it
            check_block = block.copy()
            del check_block['this_hash']
            
            meta_str = json.dumps(check_block, sort_keys=True)
            calc_hash = hashlib.sha256(meta_str.encode('utf-8')).hexdigest()
            
            if calc_hash != block['this_hash']:
                return False, i
            
            prev_hash = block['this_hash']
        return True, -1

def test_evidence_integrity():
    print("[INFO] Loading Schema...")
    load_json(METADATA_SCHEMA)
    
    chain = EvidenceChain()
    
    # 1. Build Chain
    print("  > Building evidence chain...")
    chain.add_evidence("Screenshot 1")
    chain.add_evidence("Log File A")
    chain.add_evidence("DB Dump Z")
    
    valid, _ = chain.verify()
    if not valid:
        print("[FAIL] Valid chain failed verification.")
        sys.exit(1)
    print("[PASS] Chain verified.")
    
    # 2. Tamper Content
    print("  > Attempting to break chain link...")
    # Change the prev hash of the last block to point somewhere else
    chain.chain[-1]['previous_evidence_hash'] = "BROKEN_HASH"
    
    valid, idx = chain.verify()
    if valid:
        print("[FAIL] Broken chain passed verification.")
        sys.exit(1)
    print(f"[PASS] Broken link detected at index {idx}.")

def main():
    try:
        test_evidence_integrity()
        print("\n[SUCCESS] Evidence Integrity Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
