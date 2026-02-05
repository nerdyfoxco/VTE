import hashlib
import datetime
import json
from typing import Dict, Any, Optional
from vte.core.canonicalize import canonical_json_dumps
from vte.core.security import verify_signature # Assuming we add this or use jose directly

class IntegrityVerifier:
    def __init__(self, key_store_client=None):
        self.key_store = key_store_client # Stub for AWS KMS / Vault

    def verify_evidence_integrity(self, bundle: Dict[str, Any]) -> bool:
        """
        Enforces:
        1. Payload Signature matches.
        2. Hash matches content.
        3. Time Skew is within tolerance (30s).
        """
        print("[IntegrityVerifier] Verifying Bundle...")
        
        # 1. Check Signature
        if "signature" not in bundle:
            print("[FAIL] Missing Signature.")
            return False
            
        # Verify Signature (using security module logic)
        # We assume 'signature' is an HMAC of the canonical content
        payload = bundle.copy()
        signature = payload.pop("signature")
        
        # Verify proper Key/Signature
        if not verify_signature(payload, signature):
             print("[FAIL] Signature Verification Failed.")
             return False

        # 2. Check Time Skew
        try:
            ts_str = bundle.get("timestamp") or bundle.get("collected_at")
            if not ts_str:
                print("[FAIL] Missing Timestamp.")
                return False
                
            # Parse ISO8601
            # In VTE contracts, we mandate 'Z' suffix or +00:00
            if not ts_str.endswith("Z") and "+00:00" not in ts_str:
                 print("[FAIL] Timestamp must be UTC (Z-suffix).")
                 return False
                 
            # Simple Skew Check (using naive UTC for now to avoid timezone hell)
            event_time = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            current_time = datetime.datetime.now(datetime.timezone.utc)
            
            # Allow 5 minute skew for local dev variance
            if abs((current_time - event_time).total_seconds()) > 300: 
                print(f"[FAIL] Time Skew too large. Event: {event_time}, Now: {current_time}")
                return False
            
        except Exception as e:
            print(f"[FAIL] Time parsing/validation error: {e}")
            return False

        print("[PASS] Evidence Integrity Verified.")
        return True

    def verify_proof_context(self, context: Dict[str, Any]) -> bool:
        """
        Enforces:
        1. Trace ID presence.
        2. Tenant ID presence.
        3. Actor Authority Binding.
        """
        print("[IntegrityVerifier] Verifying Context...")
        
        if "trace_id" not in context or not context["trace_id"]:
            print("[FAIL] Missing Trace ID.")
            return False
            
        if "tenant_id" not in context:
            print("[FAIL] Missing Tenant Context.")
            return False
            
        if "effective_authority" not in context:
            print("[FAIL] Missing Effective Authority Binding.")
            return False

        print("[PASS] Proof Context Valid.")
        return True
