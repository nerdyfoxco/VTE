from fastapi.testclient import TestClient
from vte.main import app
import time
import uuid
import pytest
from unittest.mock import MagicMock, patch
from vte.db import SessionLocal
from vte.orm import Unit, Property, DecisionObject
from vte.api.schema import RoleEnum, OutcomeEnum

client = TestClient(app)

def item_timestamp():
    from datetime import datetime
    return datetime.utcnow()

def test_ingestion_automation_flow():
    print("\n--- Testing Ingestion Automation (Mocked Gmail) ---")
    
    # 1. Setup: Create a Unit to be "leased"
    db = SessionLocal()
    unit_name = "Unit 999" # Unique name
    
    try:
        # 1. Setup: Dummy Decision (FK Constraint)
        decision_hash = f"setup_{uuid.uuid4()}" 
        dummy_decision = DecisionObject(
            decision_id=uuid.uuid4(),
            timestamp=item_timestamp(),
            actor_user_id="setup",
            actor_role=RoleEnum.system_bot,
            intent_action="SETUP",
            intent_target="SETUP",
            intent_params={},
            outcome=OutcomeEnum.APPROVED,
            policy_version="0",
            decision_hash=decision_hash,
            previous_hash="genesis"
        )
        db.add(dummy_decision)

        # 2. Property
        prop_id = uuid.uuid4() 
        
        prop = Property(
            property_id=prop_id,
            name="Test Property 1",
            address="123 Test Lane",
            created_at_decision_hash=decision_hash,
            updated_at_decision_hash=decision_hash
        )
        db.add(prop)

        # 2. Unit
        unit = Unit(
            unit_id=uuid.uuid4(),
            property_id=prop_id,
            name=unit_name, 
            status="VACANT",
            created_at_decision_hash=decision_hash,
            updated_at_decision_hash=decision_hash
        )
        db.add(unit)
        db.commit()
        db.refresh(unit)
        target_unit_id = unit.unit_id
        
        print(f"SETUP: Created Property '{prop.name}' & Unit '{unit_name}' (ID: {target_unit_id}) - Status: {unit.status}")
        
    finally:
        db.close()

    # 2. Mock Gmail Poller Return
    mock_email = {
        "source_id": "email_test_123",
        "subject": f"New Lease Signed for {unit_name}",
        "snippet": "Attached is the lease.",
        "sender": "newtenant@example.com",
        "date_raw": "2026-02-04"
    }

    # 3. Patch the Poller and Run Trigger
    # We patch `vte.adapters.gmail.poller.GmailPoller.poll_leases`
    
    # Also patch Engine Contracts
    mock_contract = {
        "feature_id": "ingestion_contract",
        "transitions": [
            {
                "trigger": "UPDATE_UNIT_TENANT", 
                "from": "*", 
                "to": "OCCUPIED", 
                "target_type": "unit",
                "side_effects": ["db_projection_unit_status", "db_update_tenant_info"]
            }
        ],
        "side_effects": {
            "UPDATE_UNIT_TENANT": ["db_projection_unit_status", "db_update_tenant_info"]
        }
    }

    with patch("vte.adapters.gmail.poller.GmailPoller.poll_leases", return_value=[mock_email]), \
         patch("vte.core.engine.WorkflowEngine._load_contracts", return_value={"ingestion_contract": mock_contract}):
        print("ACTION: Triggering Ingestion Agent...")
        resp = client.post("/api/v1/inventory/ingest/run")
        
        assert resp.status_code == 200
        print(f"RESPONSE: {resp.json()}")

    # 4. Verify Outcome
    db = SessionLocal()
    try:
        import uuid
        updated_unit = db.query(Unit).filter(Unit.unit_id == uuid.UUID(target_unit_id)).first()
        
        print(f"VERIFY: Unit Status is now: {updated_unit.status}")
        print(f"VERIFY: Tenant Info: {updated_unit.tenant_info}")
        
        assert updated_unit.status == "OCCUPIED"
        assert updated_unit.tenant_info["tenant_name"] == "newtenant@example.com"
        
        print("SUCCESS: Automation Test Passed.")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_ingestion_automation_flow()

def item_timestamp():
    from datetime import datetime
    return datetime.utcnow()
