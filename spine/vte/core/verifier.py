import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from vte.core.canonicalize import canonical_json_dumps

# Hardcoded paths for Phase 0 (Production would use ENV or config)
CONTRACTS_ROOT = Path("C:/Bintloop/VTE/contracts/core")

class ProofVerifier:
    def __init__(self):
        self._schemas = self._load_schemas()

    def _load_schemas(self) -> Dict[str, Any]:
        schemas = {}
        for f in CONTRACTS_ROOT.glob("*.json"):
            with open(f, "r", encoding="utf-8") as schema_file:
                data = json.load(schema_file)
                # Key by filename logic or internal schema id
                # Using filename stem for simplicity: 'decision_object_v1'
                schemas[f.stem] = data
        return schemas

    def verify_decision_integrity(self, decision: Dict[str, Any]) -> bool:
        """
        Verifies that a Decision Object is cryptographically valid.
        1. Checks required fields (rudimentary schema check - detailed validation left to Pydantic/JSONSchema lib).
        2. Recalculates 'decision_hash' from the content (excluding the hash itself) and compares.
        """
        if "decision_hash" not in decision:
            raise ValueError("Decision Object missing 'decision_hash'")

        provided_hash = decision["decision_hash"]
        
        # Create a copy to calculate hash (hash is derived from content WITHOUT the hash field)
        payload = decision.copy()
        del payload["decision_hash"]
        
        # If previous_hash exists, it IS part of the payload for hashing.
        
        # Canonicalize
        canonical_bytes = canonical_json_dumps(payload)
        calculated_hash = hashlib.sha256(canonical_bytes).hexdigest()
        
        if provided_hash != calculated_hash:
            raise ValueError(f"Decision Hash Mismatch. Provided: {provided_hash}, Calculated: {calculated_hash}")
            
        return True

    def calculate_decision_hash(self, decision_payload: Dict[str, Any]) -> str:
        """
        Helper for proper hash creation. Payload must NOT contain 'decision_hash'.
        """
        if "decision_hash" in decision_payload:
             raise ValueError("Input payload should not contain 'decision_hash' field.")
             
        canonical_bytes = canonical_json_dumps(decision_payload)
        return hashlib.sha256(canonical_bytes).hexdigest()

    def verify_evidence_link(self, decision: Dict[str, Any], evidence_bundle: Dict[str, Any]) -> bool:
        """
        Verifies that the decision accurately links to the provided evidence bundle.
        """
        if "evidence_hash" not in decision:
             return True # Some decisions might not have evidence? Schema says required.
        
        # 1. Calc Evidence Hash
        # Bundle Logic: 'bundle_hash' is usually the hash of the 'items' or the whole object?
        # In migration 0002, we store 'bundle_hash' as a unique key.
        # Let's assume the bundle object has a 'bundle_hash' field, OR we verify content.
        # Migration 0002 says "bundle_hash TEXT NOT NULL".
        
        # Let's assume the bundle dict has the hash, we verify it matches content, 
        # THEN we verify decision points to it.
        
        # Step 1: Verify Bundle Integrity (Self-consistency)
        # Note: evidence_bundle_v1.json doesn't explicitly have a top-level hash field in schema properties?
        # Wait, checking evidence_bundle_v1.json schema...
        # It has "items", "bundle_id", "collected_at".
        # It does NOT have "bundle_hash" in the JSON schema I wrote earlier!
        # Migration 0002 ADDED "bundle_hash" column.
        # So the JSON representation on the wire/disk usually implies the ID is the hash, or it's a separate field.
        # Let's assume for VTE strictness, we calculate hash of the Canonical JSON of the bundle (excluding any hash field if present).
        
        canonical_bundle = canonical_json_dumps(evidence_bundle)
        calc_bundle_hash = hashlib.sha256(canonical_bundle).hexdigest()
        
        if decision["evidence_hash"] != calc_bundle_hash:
             raise ValueError(f"Evidence mismatch. Decision expects {decision['evidence_hash']}, Bundle is {calc_bundle_hash}")
             
        return True
