import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta

class DuplicateExecutionError(Exception):
    """Raised when an execution intent is flagged as a duplicate by the idempotency manager."""
    pass

class IdempotencyMiddleware:
    """
    Phase 3 Data Plane (Heart): Stops duplicate executions of the exact same intent.
    Deterministic safety mechanism that caches intent hashes.
    """
    def __init__(self, default_ttl_seconds: int = 3600):
        self.default_ttl = timedelta(seconds=default_ttl_seconds)
        # In-memory store for demonstration. A production implementation connects to Redis.
        self._store: Dict[str, datetime] = {}

    def _generate_hash(self, workspace_id: str, action_type: str, intent_payload: Dict[str, Any]) -> str:
        """Generates a deterministic SHA-256 hash of the execution intent."""
        # Sort keys to ensure deterministic dictionary hashing
        payload_str = json.dumps(intent_payload, sort_keys=True)
        raw_intent = f"{workspace_id}|{action_type}|{payload_str}"
        return hashlib.sha256(raw_intent.encode('utf-8')).hexdigest()

    def check_and_record(self, workspace_id: str, action_type: str, intent_payload: Dict[str, Any]) -> str:
        """
        Calculates intent hash. If hash exists and is within TTL, raises DuplicateExecutionError.
        Otherwise, records the hash and returns it.
        """
        intent_hash = self._generate_hash(workspace_id, action_type, intent_payload)
        now = datetime.now(timezone.utc)
        
        if intent_hash in self._store:
            expiry = self._store[intent_hash]
            if now < expiry:
                raise DuplicateExecutionError(f"Idempotency Guard: Execution block {intent_hash} is already registered and active.")
            else:
                # TTL expired, safe to execute again
                pass
                
        # Record new intent with TTL
        self._store[intent_hash] = now + self.default_ttl
        return intent_hash
