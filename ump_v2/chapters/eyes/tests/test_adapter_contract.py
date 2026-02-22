import sys
import unittest
from datetime import datetime, timezone
from uuid import uuid4
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from adapter_contract import BaseAdapter, AdapterDriftError

class CompliantAdapter(BaseAdapter):
    def fetch_raw_data(self):
        return {"external_id": 999, "status": "active"}
        
    def build_envelope(self, raw_data):
        return {
            "workspace_id": "tenant_1",
            "work_item_id": "task_1",
            "correlation_id": str(uuid4()),
            "organ_source": "eyes",
            "organ_target": "brain",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": raw_data
        }

class DriftingAdapter(BaseAdapter):
    def fetch_raw_data(self):
        return {"external_id": 111}
        
    def build_envelope(self, raw_data):
        # Oops! Forgot workspace_id, which is an invariant
        return {
            "work_item_id": "task_1",
            "correlation_id": str(uuid4()),
            "organ_source": "eyes",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": raw_data
        }

class TestAdapterContract(unittest.TestCase):

    def test_compliant_adapter_returns_envelope(self):
        adapter = CompliantAdapter()
        envelope = adapter.ingest()
        self.assertEqual(envelope.workspace_id, "tenant_1")
        self.assertEqual(envelope.payload["external_id"], 999)

    def test_drifting_adapter_throws_drift_error(self):
        adapter = DriftingAdapter()
        with self.assertRaises(AdapterDriftError) as context:
            adapter.ingest()
            
        self.assertIn("Adapter Drift Detected", str(context.exception))
        self.assertIn("workspace_id", str(context.exception))

if __name__ == '__main__':
    unittest.main()
