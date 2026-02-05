from fastapi.testclient import TestClient
from vte.main import app
from vte.db import SessionLocal
from vte.orm import DecisionObject, Unit, Property
from vte.api.schema import OutcomeEnum
import uuid
import time
from unittest.mock import MagicMock, patch

client = TestClient(app)

def test_write_note_execution_flow():
    print("\n--- Testing 'Write Note' Action Execution ---")
    
    # 1. Setup: Create a Unit to attach note to
    db = SessionLocal()
    unit_id = uuid.uuid4()
    
    # Create Dummy Prop/Decision for FK
    setup_hash = f"setup_{uuid.uuid4()}"
    decision = DecisionObject(
        decision_id=uuid.uuid4(),
        timestamp="2024-01-01",
        actor_user_id="test",
        actor_role="admin",
        intent_action="SETUP",
        intent_target="SETUP",
        intent_params={},
        outcome=OutcomeEnum.APPROVED,
        policy_version="0",
        decision_hash=setup_hash,
        previous_hash="genesis"
    )
    db.add(decision)
    
    prop = Property(property_id=uuid.uuid4(), name="Test Prop", created_at_decision_hash=setup_hash, updated_at_decision_hash=setup_hash)
    db.add(prop)
    
    unit = Unit(unit_id=unit_id, property_id=prop.property_id, name="101", status="OCCUPIED", created_at_decision_hash=setup_hash, updated_at_decision_hash=setup_hash)
    db.add(unit)
    db.commit()

    # 2. Mock AppFolio Client
    # We mock the class inside vte.tasks
    with patch("vte.tasks.AppFolioClient") as MockClientClass:
        mock_instance = MockClientClass.return_value
        mock_instance.navigate_to_tenant.return_value = True
        mock_instance.write_note.return_value = True
        
        # 3. Submit Decision via API (triggering execution)
        # Note: In real app, API triggers Celery task asynchronously. 
        # In test, if celery is eager, it runs synchronously. 
        # Or we can verify the 'execute_decision' task logic directly by importing it.
        
        # Let's call the TASK function directly to test the logic (ignoring Redis/Celery routing for now)
        from vte.tasks import execute_decision
        
        # Create the decision in DB first (simulating API)
        action_id = uuid.uuid4()
        action_decision = DecisionObject(
            decision_id=action_id,
            timestamp="2024-01-01T12:00:00Z",
            actor_user_id="ui_user",
            actor_role="admin",
            intent_action="write_note",
            intent_target=str(unit_id),
            intent_params={"content": "Test Note Verify", "dry_run": True},
            outcome=OutcomeEnum.APPROVED, # Triggers execution!
            policy_version="1.0",
            decision_hash=f"hash_{action_id}",
            previous_hash=setup_hash
        )
        db.add(action_decision)
        db.commit()
        
        # Run Task
        print(f"Executing Task for Decision {action_id}")
        result = execute_decision(str(action_id))
        
        # 4. Verify
        print(f"Task Result: {result}")
        
        # Check Mock Calls
        mock_instance.start.assert_called_once()
        mock_instance.navigate_to_tenant.assert_called_with(str(unit_id))
        mock_instance.write_note.assert_called_with("Test Note Verify", dry_run=True)
        mock_instance.close.assert_called_once()
        
        assert result["status"] == "success"
        assert result["action"] == "write_note"
        print("SUCCESS: Write Note Logic Verified")

    db.close()

if __name__ == "__main__":
    test_write_note_execution_flow()
