import sys
import unittest
from uuid import uuid4
from datetime import datetime, timezone
from pathlib import Path

current_dir = Path(__file__).resolve().parent
uml_v2_root = current_dir.parent.parent
sys.path.insert(0, str(uml_v2_root))

from foundation.src.security.correlation_guard import validate_envelope, PipeEnvelopeRejectError, PipeEnvelope

def get_valid_payload():
    return {
        "workspace_id": "tenant_123",
        "work_item_id": "task_abc",
        "correlation_id": str(uuid4()),
        "organ_source": "eyes",
        "organ_target": "brain",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "policy_version": "v1.0.0",
        "payload": {"key": "value"}
    }

class TestCorrelationGuard(unittest.TestCase):

    def test_valid_payload_passes(self):
        payload = get_valid_payload()
        envelope = validate_envelope(payload)
        self.assertIsInstance(envelope, PipeEnvelope)
        self.assertEqual(envelope.workspace_id, "tenant_123")

    def test_missing_workspace_id_fails(self):
        payload = get_valid_payload()
        del payload["workspace_id"]
        with self.assertRaises(PipeEnvelopeRejectError) as context:
            validate_envelope(payload)
        self.assertIn("workspace_id", str(context.exception))

    def test_missing_correlation_id_fails(self):
        payload = get_valid_payload()
        del payload["correlation_id"]
        with self.assertRaises(PipeEnvelopeRejectError) as context:
            validate_envelope(payload)
        self.assertIn("correlation_id", str(context.exception))

    def test_invalid_uuid_correlation_id_fails(self):
        payload = get_valid_payload()
        payload["correlation_id"] = "not-a-uuid"
        with self.assertRaises(PipeEnvelopeRejectError):
            validate_envelope(payload)

    def test_extra_top_level_keys_fails(self):
        payload = get_valid_payload()
        payload["sneaky_hacker_key"] = "bypass_guards"
        with self.assertRaises(PipeEnvelopeRejectError) as context:
             validate_envelope(payload)
        self.assertIn("Extra inputs are not permitted", str(context.exception))

if __name__ == '__main__':
    unittest.main()
