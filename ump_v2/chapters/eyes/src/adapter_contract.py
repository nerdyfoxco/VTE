from abc import ABC, abstractmethod
from typing import Dict, Any
import sys
from pathlib import Path

# Add foundation to path to consume PipeEnvelope components
current_dir = Path(__file__).resolve().parent
foundation_dir = current_dir.parent.parent.parent / "foundation" / "src"
sys.path.insert(0, str(foundation_dir))

from security.correlation_guard import PipeEnvelope, validate_envelope, PipeEnvelopeRejectError

class AdapterDriftError(Exception):
    """Raised when an external adapter yields data that breaks the Pipe Envelope Contract."""
    pass

class BaseAdapter(ABC):
    """
    Phase 3 Data Plane (Eyes): External adapter base class.
    Mechanically enforces that all eyes wrap unstructured data into strict PipeEnvelopes
    before passing it onto the Spine/Brain.
    """
    
    @abstractmethod
    def fetch_raw_data(self) -> Dict[str, Any]:
        """Subclasses implement this to get unstructured external data."""
        pass
        
    @abstractmethod
    def build_envelope(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Subclasses implement this to map raw payload to the PipeEnvelope schema."""
        pass

    def ingest(self) -> PipeEnvelope:
        """
        The authoritative entrypoint. 
        Calls subclass logic, then forces the result through the Canonical Pydantic guard.
        If it fails, it halts ingestion with an explicit Drift Error.
        """
        raw = self.fetch_raw_data()
        envelope_dict = self.build_envelope(raw)
        
        try:
            # Deterministic gating: Force validate against the centralized Pydantic guard from Phase 0
            validated_envelope = validate_envelope(envelope_dict)
            return validated_envelope
        except PipeEnvelopeRejectError as e:
            # Reclassify the generic validation error into a structural system error from the Organ
            raise AdapterDriftError(f"Adapter Drift Detected: The adapter '{self.__class__.__name__}' failed to produce a valid PipeEnvelope. Details: {e}")
