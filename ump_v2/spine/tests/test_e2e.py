import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
import uuid
import datetime
from datetime import timezone

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from main import app

class TestE2EIntegration(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_full_pipeline_happy_path(self):
        payload = {
            "workspace_id": "ws_123",
            "work_item_id": "task_abc",
            "correlation_id": str(uuid.uuid4()),
            "organ_source": "eyes",
            "organ_target": "brain",
            "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
            "payload": {
                 "user_id": "user_1",
                 "status": "delinquent",
                 "ssn": "123-45-6789"
            }
        }
        
        response = self.client.post("/ingest", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["action"], "PROCEED")
        self.assertEqual(data["decision"], "CONTACT")
        self.assertEqual(data["state_machine_status"], "DECISION")
        
    def test_idempotency_blocks_duplicates(self):
        payload = {
            "workspace_id": "ws_999",
            "work_item_id": "task_xyz",
            "correlation_id": str(uuid.uuid4()),
            "organ_source": "eyes",
            "organ_target": "brain",
            "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
            "payload": {
                 "user_id": "user_1",
                 "status": "delinquent"
            }
        }
        
        # First request
        r1 = self.client.post("/ingest", json=payload)
        self.assertEqual(r1.status_code, 200)
        
        # Second immediate request
        r2 = self.client.post("/ingest", json=payload)
        self.assertEqual(r2.status_code, 400)
        self.assertIn("Idempotency Guard", r2.json()["detail"])

    def test_compliance_blocks_eu_without_consent(self):
        payload = {
            "workspace_id": "ws_123",
            "work_item_id": "task_abc",
            "correlation_id": str(uuid.uuid4()),
            "organ_source": "eyes",
            "organ_target": "brain",
            "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
            "payload": {
                 "user_id": "user_2",
                 "status": "delinquent"
            }
        }
        
        response = self.client.post("/ingest", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Compliance Blocked", response.json()["detail"])

    def test_policy_engine_stops_legal_representation(self):
        payload = {
            "workspace_id": "ws_124",
            "work_item_id": "task_legal",
            "correlation_id": str(uuid.uuid4()),
            "organ_source": "eyes",
            "organ_target": "brain",
            "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
            "payload": {
                 "user_id": "user_1",
                 "has_legal": True
            }
        }
        
        response = self.client.post("/ingest", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["action"], "TERMINATE")
        self.assertEqual(data["decision"], "STOP")
        self.assertEqual(data["state_machine_status"], "STOP")
        
    def test_missing_workspace_id_fails_envelope_validation(self):
        payload = {
            # "workspace_id": "ws_124", MISSING
            "work_item_id": "task_legal",
            "correlation_id": str(uuid.uuid4()),
            "organ_source": "eyes",
            "organ_target": "brain",
            "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
            "payload": {
                 "user_id": "user_1",
                 "has_legal": True
            }
        }
        response = self.client.post("/ingest", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Field required", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
