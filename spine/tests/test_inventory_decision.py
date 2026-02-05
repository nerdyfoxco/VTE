from fastapi.testclient import TestClient
from vte.main import app
from vte.api.schema import RoleEnum, OutcomeEnum, DecisionDraft, Actor, Intent
import uuid
import time
import pytest
from vte.db import SessionLocal
from vte.orm import Property, Unit, DecisionObject

client = TestClient(app)

# Mock Auth for testing
def get_mock_claims():
    return {"user_id": "test_admin", "role": "super_admin"}

# We need to override the dependency in a real test harness, 
# but for this simple script we can rely on the fact that our local dev environment allows admin bypass or we mock it.
# Actually, `test_client` alone might fail auth if we don't override.
# Let's rely on the fact that we can post to /decisions with a valid token if we implement login, 
# OR just manually invoke the logic if we want to unit test the projection.

# Integration Test: Decision -> Task -> DB
def test_inventory_projection_flow():
    db = SessionLocal()
    try:
        # 1. Manually Create a Decision Object (Simulating API + Policy Engine success)
        # We do this to isolate the "Projection" logic from "Policy" logic which might reject random inputs.
        
        # However, to be thorough, let's use the API if possible.
        # But auth is hard to mock in a single script without `app.dependency_overrides`.
        
        prop_id = str(uuid.uuid4())
        prop_name = f"Test Property {int(time.time())}"
        
        decision_id = str(uuid.uuid4())
        decision_hash = f"hash_{decision_id}"
        
        db_decision = DecisionObject(
            decision_id=uuid.UUID(decision_id),
            timestamp=item_timestamp(),
            actor_user_id="tester",
            actor_role=RoleEnum.super_admin,
            actor_session_id="sess_1",
            intent_action="REGISTER_PROPERTY",
            intent_target=prop_id,
            intent_params={"name": prop_name, "address": "123 Test St"},
            evidence_hash="test_evidence",
            outcome=OutcomeEnum.APPROVED,
            policy_version="1.0",
            decision_hash=decision_hash,
            previous_hash="genesis"
        )
        db.add(db_decision)
        db.commit()
        
        # 2. Invoke Task Manually via Engine
        from vte.tasks import execute_decision
        from unittest.mock import patch
        
        # Patching engine contracts
        mock_contract = {
            "feature_id": "inventory",
            "transitions": [{"trigger": "REGISTER_PROPERTY", "from": "*", "to": "*", "target_type": "property", "side_effects": ["db_projection_property"]}],
            "side_effects": {"REGISTER_PROPERTY": ["db_projection_property"]}
        }
        
        with patch("vte.core.engine.WorkflowEngine._load_contracts", return_value={"inventory": mock_contract}):
             execute_decision(str(decision_id))
        
        # 3. Verify Projection
        prop = db.query(Property).filter(Property.property_id == uuid.UUID(prop_id)).first()
        assert prop is not None, "Property should have been projected"
        assert prop.name == prop_name
        assert prop.created_at_decision_hash == decision_hash
        
        print(f"SUCCESS: Property {prop_name} projected successfully.")
        
        # 4. Verify API Read
        # We need to commit first so the generic client thread sees it? 
        # Actually same thread/same DB in this script context usually.
        resp = client.get(f"/api/v1/inventory/properties/{prop_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == prop_name
        
        print("SUCCESS: API Read confirmed.")
        
    finally:
        db.close()

def item_timestamp():
    from datetime import datetime
    return datetime.utcnow()

if __name__ == "__main__":
    try:
        test_inventory_projection_flow()
        print("Inventory Decision Flow: PASSED")
    except Exception as e:
        print(f"Inventory Decision Flow: FAILED ({e})")
        import traceback
        traceback.print_exc()
