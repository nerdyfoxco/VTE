import json
from typing import Any, Union

def canonical_json_dumps(data: Any) -> bytes:
    """
    Serializes data to Canonical JSON format (RFC 8785 compliant).
    
    Rules:
    - Keys are sorted lexicographically.
    - No whitespace (separators are used efficiently).
    - Output is UTF-8 encoded bytes.
    - Floats are NOT supported to prevent precision drift (using Decimal or string is preferred in VTE).
    """
    # Fail fast on floats to prevent non-deterministic serialization
    if _contains_float(data):
        raise ValueError("Floats are not permitted in Canonical JSON for VTE. Use strings or integers.")

    # sort_keys=True ensures deterministic ordering
    # separators=(',', ':') removes whitespace
    # ensure_ascii=False allows direct UTF-8 characters (required for RFC 8785)
    return json.dumps(
        data,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False
    ).encode('utf-8')

def _contains_float(data: Any) -> bool:
    """Recursively checks for float types."""
    if isinstance(data, float):
        return True
    if isinstance(data, dict):
        return any(_contains_float(v) for v in data.values())
    if isinstance(data, list):
        return any(_contains_float(x) for x in data)
    return False
