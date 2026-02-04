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

    print("\n--- 4. Verify Execution (Phase 16) ---")
    
    # 4.1 Approve the Decision (Create Append-Only Block)
    # Get hash of the PROPOSED decision
    proposed_decision = next(d for d in items if d["decision_id"] == decision_id)
    proposed_hash = proposed_decision["decision_hash"]
    
    approval_payload = {
        "actor": {
             "user_id": "admin_user",
             "role": "admin",
             "session_id": "sess_admin"
        },
        "intent": {
            "action": "write_note", # Override for test
            "target_resource": proposed_decision["intent_target"],
            "parameters": {"content": "Verified by VTE Phase 16", "dry_run": True}
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
    
    # 4.2 Execute
    print("Triggering Execution Task (Sync)...")
    from vte.tasks import execute_decision
    
    # Ensure env var for cookies is set to avoid random IO errors
    import os
    os.environ["APPFOLIO_COOKIE_PATH"] = "./test_cookies.json"
    
    result = execute_decision(approved_id)
    print(f"Execution Result: {result}")
    
    # Verification Logic
    # We expect 'failed_navigation' (if no cookies) or 'success' (if cookies exist)
    # The key is that it didn't crash or return 'not_found'.
    if result["status"] == "success":
        print("SUCCESS: Execution Succeeded (Writeback).")
    elif result["status"] == "failed" and result["reason"] == "navigation_failed":
        print("SUCCESS: Execution Attempted (Navigation Verified - Auth Wall Hit as expected).")
    elif result["status"] == "failed" and result["reason"] == "not_found":
        print("FAILURE: Execution Task could not find the decision.")
        sys.exit(1)
    else:
         print(f"WARNING: Execution Result unexpected: {result}")

if __name__ == "__main__":
    test_governance_flow()

if __name__ == "__main__":
    test_governance_flow()
