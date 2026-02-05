from fastapi.testclient import TestClient
from vte.main import app
import time
import os
import uuid
from vte.api.schema import RoleEnum, OutcomeEnum
from vte.orm import Property
from vte.db import SessionLocal

client = TestClient(app)

def test_appfolio_wiring():
    print("\n--- Testing AppFolio Wiring ---")
    
    # 1. Save Creds
    payload = {"username": "test_user", "password": "test_password"}
    resp = client.post("/api/v1/connect/appfolio/credentials", json=payload)
    
    if resp.status_code == 200:
        print("SUCCESS: Credentials Saved Endpoint Works.")
        # Verify file
        if os.path.exists("appfolio_creds.json"):
            print("SUCCESS: File created.")
            os.remove("appfolio_creds.json") # Cleanup
        else:
            print("FAILURE: File not created.")
    else:
        print(f"FAILURE: {resp.status_code} {resp.text}")

def test_inventory_api_wiring():
    print("\n--- Testing Inventory API Wiring ---")
    
    # 1. Read (Should be empty or have previous test data)
    resp = client.get("/api/v1/inventory/properties")
    assert resp.status_code == 200
    print(f"SUCCESS: GET /properties returned {len(resp.json())} items")

    # 2. Write (Decision) -> Projection -> Read
    prop_name = f"Wiring Test {int(time.time())}"
    
    # Manually inject decision/projection to simulate the "Async Worker"
    # (Since we can't easily wait for Celery in this script)
    db = SessionLocal()
    from vte.orm import DecisionObject
    # from vte.tasks import handle_inventory_projection
    
    decision_hash = f"hash_{uuid.uuid4()}"
    decision = DecisionObject(
        decision_id=uuid.uuid4(),
        timestamp=item_timestamp(),
        actor_user_id="ui_wiring",
        actor_role=RoleEnum.user,
        intent_action="REGISTER_PROPERTY",
        intent_target=str(uuid.uuid4()),
        intent_params={"name": prop_name},
        outcome=OutcomeEnum.APPROVED,
        policy_version="1.0",
        decision_hash=decision_hash,
        previous_hash="chain"
    )
    db.add(decision)
    db.commit()
    
    # handle_inventory_projection(decision, db) # Force Projection
    
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
         execute_decision(str(decision.decision_id))
    db.close()
    
    # 3. Read Again
    resp = client.get("/api/v1/inventory/properties")
    items = resp.json()
    found = any(i["name"] == prop_name for i in items)
    
    if found:
        print(f"SUCCESS: Property '{prop_name}' visible in API.")
    else:
        print("FAILURE: Property not found in API.")

def item_timestamp():
    from datetime import datetime
    return datetime.utcnow()

if __name__ == "__main__":
    test_appfolio_wiring()
    test_inventory_api_wiring()
