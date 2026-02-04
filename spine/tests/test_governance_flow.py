from fastapi.testclient import TestClient
from vte.main import app
import sys
import uuid

client = TestClient(app)

def test_governance_flow():
    print("\n--- 1. Create Evidence Bundle ---")
    evidence_payload = {
        "normalization_schema": "test_schema",
        "items": [
            {
                "source": "test",
                "type": "row",
                "data": {"foo": "bar"},
                "sha256": "hash_123"
            }
        ]
    }
    resp = client.post("/api/v1/evidence", json=evidence_payload)
    if resp.status_code != 201:
        print(f"Evidence Failed: {resp.text}")
        sys.exit(1)
    evidence_hash = resp.json()["bundle_hash"]
    print(f"Evidence Hash: {evidence_hash}")

    print("\n--- 2. Create PROPOSED Decision (Agent) ---")
    decision_payload = {
        "actor": {
            "user_id": "agent_007",
            "role": "system_bot",
            "session_id": "sess_agent"
        },
        "intent": {
            "action": "refund_user",
            "target_resource": "txn_999",
            "parameters": {"amount": 50}
        },
        "evidence_hash": evidence_hash,
        "outcome": "PROPOSED",
        "policy_version": "v1.0"
    }
    
    # We need a valid JWT token usually, but for TestClient with the dummy Auth override or skip?
    # Wait, routes.py uses `Depends(get_current_user_claims)`.
    # I need to mock that dependency or use a token.
    # For now, let's see if we fail 403.
    # Ah, I'll update main.py to allow BYPASS for testing or use a valid token.
    # Actually, let's just use the `auth` endpoint to get a token if it exists.
    # Or mock the override.
    
    # Mocking override in app
    from vte.api.deps import get_current_user_claims
    app.dependency_overrides[get_current_user_claims] = lambda: {
        "user_id": "agent_007", 
        "role": "system_bot", 
        "permissions": ["*"]
    }
    
    resp = client.post("/api/v1/decisions", json=decision_payload)
    if resp.status_code != 201:
        print(f"Decision Creation Failed: {resp.text}")
        sys.exit(1)
        
    data = resp.json()
    decision_id = data["decision_id"]
    print(f"Created Decision {decision_id} (PROPOSED)")
    
    print("\n--- 3. Fetch Pending Decisions (Admin) ---")
    resp = client.get("/api/v1/decisions?status=PROPOSED")
    if resp.status_code != 200:
        print(f"Fetch Failed: {resp.text}")
        sys.exit(1)
        
    items = resp.json()
    print(f"Pending Count: {len(items)}")
    found = any(d["decision_id"] == decision_id for d in items)
    
    if found:
        print("SUCCESS: Found newly created PROPOSED decision.")
    else:
        print("FAILURE: Did not find decision in list.")
        sys.exit(1)

    print("\n--- 4. Verify Execution (Phase 17: HITL) ---")
    
    # 4.1 Mock the Client & Enable Eager Mode
    from unittest.mock import patch
    from vte.worker import celery_app
    
    # Enable Eager Mode (Synchronous Worker)
    celery_app.conf.task_always_eager = True
    print("Celery Eager Mode: ON")

    # Mock AppFolioClient to verify it gets called by the backend
    with patch("vte.tasks.AppFolioClient") as MockClient:
        # Setup Mock
        mock_instance = MockClient.return_value
        mock_instance.navigate_to_tenant.return_value = True
        mock_instance.write_note.return_value = True
        
        # 4.2 Approve the Decision (Should trigger execution)
        print("Approving Decision (API)...")
        
        # Get hash of the PROPOSED decision
        proposed_decision = next(d for d in items if d["decision_id"] == decision_id)
        
        approval_payload = {
            "actor": {
                 "user_id": "admin_user",
                 "role": "admin",
                 "session_id": "sess_admin"
            },
            "intent": {
                "action": "write_note",
                "target_resource": proposed_decision["intent_target"],
                "parameters": {"content": "Verified by VTE Phase 17 HITL", "dry_run": True}
            },
            "evidence_hash": evidence_hash,
            "outcome": "APPROVED",
            "policy_version": "v1.0"
        }
        
        resp = client.post("/api/v1/decisions", json=approval_payload)
        if resp.status_code != 201:
            print(f"Approval Failed: {resp.text}")
            sys.exit(1)
            
        approved_id = resp.json()["decision_id"]
        print(f"Created Decision {approved_id} (APPROVED)")
        
        # 4.3 Verify Side Effect
        print("Verifying Side Effect (Mock Call)...")
        if mock_instance.write_note.called:
            print("SUCCESS: AppFolioClient.write_note() was triggered AUTOMATICALLY!")
            args, kwargs = mock_instance.write_note.call_args
            print(f"Called with: {args} {kwargs}")
        else:
            print("FAILURE: AppFolioClient was NOT called.")
            sys.exit(1)

if __name__ == "__main__":
    test_governance_flow()

if __name__ == "__main__":
    test_governance_flow()
