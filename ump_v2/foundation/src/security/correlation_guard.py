from pydantic import BaseModel, ConfigDict, Field, UUID4, ValidationError
from datetime import datetime
from typing import Any, Dict, Optional

class PipeEnvelopeRejectError(Exception):
    """Raised when an incoming payload fails the universal pipe envelope validation."""
    pass

class PipeEnvelope(BaseModel):
    """
    Pydantic representation of the universal pipe-envelope.schema.json.
    Enforces Phase 0 runtime invariants for all Organs.
    """
    model_config = ConfigDict(extra='forbid')

    workspace_id: str = Field(..., description="Hard requirement for tenant isolation.")
    work_item_id: str = Field(..., description="Identifier for the end-to-end trace.")
    correlation_id: UUID4 = Field(..., description="Universally Unique Identifier for tracing.")
    organ_source: str = Field(...)
    organ_target: Optional[str] = Field(default=None)
    timestamp: datetime = Field(...)
    policy_version: Optional[str] = Field(default=None)
    payload: Dict[str, Any] = Field(...)

def validate_envelope(raw_payload: Dict[str, Any]) -> PipeEnvelope:
    """
    Validates a raw dictionary against the universal pipe envelope contract.
    Fails closed if the payload violates invariants (e.g. missing workspace_id).
    
    Args:
        raw_payload: The untrusted incoming pipe payload.
        
    Returns:
        A validated PipeEnvelope object.
        
    Raises:
        PipeEnvelopeRejectError if validation fails.
    """
    try:
        validated = PipeEnvelope(**raw_payload)
        return validated
    except ValidationError as e:
        # We explicitly catch pydantic errors and morph them into our taxonomy
        error_msg = f"PIPELINE REJECTED: Envelope Contract Violation: {e}"
        raise PipeEnvelopeRejectError(error_msg)
