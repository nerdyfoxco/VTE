import hashlib
import json
from datetime import datetime

# Simulates the logic of appending to an immutable hash chain
# In a real DB, this would be part of the 'evidence_bundles' insertion transaction

class EvidenceWriter:
    def __init__(self, db_session):
        self.db = db_session

    def compute_sha256(self, data: dict) -> str:
        """Canonicalize and Hash"""
        canonical_json = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    def persist_evidence(self, bundle: dict) -> str:
        """
        Accepts a raw bundle, calculates its hash, links it to previous (simulated),
        and returns the finalized chain hash.
        """
        # 1. Get Previous Hash (Stub: In real app, query `SELECT bundle_hash FROM ... ORDER BY collected_at DESC LIMIT 1`)
        previous_hash = "GENESIS_HASH_0000000000000000000000" 
        
        # 2. Enrich Bundle
        bundle["previous_hash"] = previous_hash
        bundle["processed_at"] = datetime.utcnow().isoformat() + "Z"
        
        # 3. Calculate Final Chain Hash
        final_hash = self.compute_sha256(bundle)
        
        # 4. Write to DB (Stub)
        # self.db.add(EvidenceBundle(..., bundle_hash=final_hash)
        
        print(f"[EvidenceWriter] Persisted Bundle. Hash: {final_hash}")
        return final_hash

if __name__ == "__main__":
    # Test Stub
    writer = EvidenceWriter(None)
    test_bundle = {"data": "test_txn_123", "amount": 100}
    print(writer.persist_evidence(test_bundle))
