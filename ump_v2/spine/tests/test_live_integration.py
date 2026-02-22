import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from main import app

class TestLiveIntegration(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_sync_gmail_endpoint_flows_to_hands(self):
        # We don't send a payload; the Adapter simulates fetching from Gmail automatically.
        response = self.client.post("/sync-gmail")
        
        # The mock email has "past due" returning "delinquent", but ALSO has "legal" making has_legal=True.
        # The policy engine precedence rules dictate STOP overrides all.
        # So we expect action to be TERMINATE and Hands to be Skipped.
        
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        
        self.assertEqual(data["vte_sync_status"], "OK")
        self.assertEqual(data["brain_engine_result"]["decision"], "STOP")
        self.assertEqual(data["brain_engine_result"]["action"], "TERMINATE")
        self.assertIn("Skipped", data["hands_execution_result"])

if __name__ == "__main__":
    unittest.main()
