import sys
import os
import json
from fastapi.testclient import TestClient


# Add cwd to path for vte package resolution
sys.path.append(os.getcwd())

try:
    from vte.main import app
except ImportError as e:
    print(f"FAIL: Could not import vte.main: {e}")
    sys.exit(1)

client = TestClient(app)

# Mock Auth
from vte.api.deps import get_current_user_claims
app.dependency_overrides[get_current_user_claims] = lambda: {"user_id": "Kevin", "role": "admin", "session_id": "test"}

def verify_queue_api():
    print("Verifying Layer 4: Backend Unified Queue API...")
    
    # 0. Seed Data (Since DB is wiped on startup)
    print("Seeding test data...")
    seed_payload = {
        "actor": {
            "user_id": "Kevin",
            "role": "admin", 
            "session_id": "test-session"
        },
        "intent": {
            "action": "Review High Priority Item",
            "target_resource": "item-123",
            "parameters": {}
        },
        "evidence_hash": "hash_123",
        "outcome": "PROPOSED", # Status PENDING in Queue
        "policy_version": "v1.0"
    }
    res = client.post("/api/v1/decisions", json=seed_payload)
    if res.status_code != 201:
        print(f"FAIL: Could not seed data. Status {res.status_code}: {res.text}")
        sys.exit(1)

    # 1. Verify Queue
    response = client.get("/api/v1/queue")
    
    if response.status_code != 200:
        print(f"FAIL: API returned status {response.status_code}")
        print(response.text)
        sys.exit(1)
        
    items = response.json()
    print(f"PASS: API returned {len(items)} items.")
    
    # Contract Check
    for item in items:
        # Check required fields from unified_queue_truth_v1.json + enriched fields
        required_fields = ["id", "priority", "sla_deadline", "title", "status"]
        for field in required_fields:
            if field not in item:
                print(f"FAIL: Item {item.get('id')} missing required field '{field}'")
                sys.exit(1)
                
    print("PASS: API response structure validates against contract.")
    
    # Check specific data point
    kevins_task = next((i for i in items if i["assigned_to"] == "Kevin"), None)
    if not kevins_task:
        print("FAIL: No tasks assigned to Kevin found.")
        sys.exit(1)
        
    print(f"PASS: Found task for Kevin: {kevins_task['title']}")
    print("LAYER 4 LOGIC VERIFIED.")

if __name__ == "__main__":
    verify_queue_api()
