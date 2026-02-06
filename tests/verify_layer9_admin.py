import sys
import os
import json
import unittest
from fastapi.testclient import TestClient

# Add apps/backend-core to path
sys.path.append(os.path.join(os.getcwd(), "apps", "backend-core"))

try:
    from spine.main import app
except ImportError as e:
    print(f"FAIL: Could not import spine.main: {e}")
    sys.exit(1)

client = TestClient(app)

class TestIdentityAdmin(unittest.TestCase):
    
    def test_impersonate_requires_dual_approval(self):
        # 1. Attempt without secondary approver (Should Fail)
        payload = {
            "action": "IMPERSONATE_USER",
            "target_user_id": "user_123",
            "reason": "Support investigation"
        }
        response = client.post("/api/v1/admin/execute", json=payload)
        self.assertEqual(response.status_code, 403, "Must return 403 Forbidden without dual approval")
        self.assertIn("Dual Approval", response.json()["detail"])

        # 2. Attempt with secondary approver (Should Succeed)
        payload["secondary_approver_id"] = "admin_456"
        response = client.post("/api/v1/admin/execute", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_impersonate_self_approval_blocked(self):
        # Prevent secondary approver == target
        payload = {
            "action": "IMPERSONATE_USER",
            "target_user_id": "user_123",
            "secondary_approver_id": "user_123", # Self-approval attempt
            "reason": "I want to be me"
        }
        response = client.post("/api/v1/admin/execute", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("cannot be the target", response.json()["detail"])

    def test_unauthorized_action(self):
        payload = {
            "action": "DELETE_EVERYTHING", 
            "target_user_id": "world",
            "reason": "oops"
        }
        response = client.post("/api/v1/admin/execute", json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
