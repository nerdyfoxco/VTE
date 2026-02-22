import json
import logging
from typing import Any, Dict, List
from pathlib import Path

logger = logging.getLogger(__name__)

class RedactionEngine:
    """
    Phase 0 System Invariant: Prevent PII leakage to logs or AI payloads.
    Loads canonical redaction rules and recursively scrubs dictionaries.
    """
    def __init__(self, rules_path: str = None):
        if rules_path is None:
            # Default to the adjacent rules file
            rules_path = Path(__file__).parent / "redaction_rules.json"
            
        with open(rules_path, "r") as f:
            self.rules = json.load(f)
            
        self.exact_keys = set(self.rules.get("redact_keys_exact", []))
        self.partial_keys = set(self.rules.get("redact_keys_partial", []))
        self.replacement = self.rules.get("replacement_string", "[REDACTED]")
        
    def redact(self, payload: Any) -> Any:
        """
        Recursively traverse the payload and replace sensitive values.
        Returns a new redacted object, leaving original intact.
        """
        if isinstance(payload, dict):
            return {k: self._scrub_value(k, v) for k, v in payload.items()}
        elif isinstance(payload, list):
            return [self.redact(item) for item in payload]
        return payload
        
    def _scrub_value(self, key: str, value: Any) -> Any:
        key_lower = key.lower()
        
        # If the value is a nested dict/list, recurse first
        if isinstance(value, (dict, list)):
            return self.redact(value)
            
        # Exact match (e.g., total redaction of SSN)
        if key_lower in self.exact_keys:
            return self.replacement
            
        # Partial match (e.g., if key CONTAINS 'phone' or 'email')
        for partial_key in self.partial_keys:
            if partial_key in key_lower:
                return self.replacement
                
        return value

# Global singleton for easy import across modules
_engine = None

def redact_payload(payload: Any) -> Any:
    """Convenience function to redact a payload using the default rules."""
    global _engine
    if _engine is None:
        _engine = RedactionEngine()
    return _engine.redact(payload)
