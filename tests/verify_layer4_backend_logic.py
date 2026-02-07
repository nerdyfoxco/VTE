import sys
import os
import json
from fastapi.testclient import TestClient

try:
    from vte.main import app
except ImportError as e:
    print(f"FAIL: Could not import vte.main: {e}")
    sys.exit(1)

client = TestClient(app)

def verify_queue_api():
    print("Verifying Layer 4: Backend Unified Queue API...")
    
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
