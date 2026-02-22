import sys
from pathlib import Path

# Fix module imports completely independently of pytest
base_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(base_dir / "src"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    import uuid
    print("--- VTE 2.0 APPFOLIO ENDPOINT VERIFICATION ---")
    
    # CASE 1: Standard Delinquency -> PROCEED
    payload = {
        "tenant_id": "tnt_standard_1", "work_item_id": f"wi_{uuid.uuid4()}", "tenant_name": "Standard Kevin", "status": "delinquent",
        "tenant_tags": ["pet owner", "renters insurance"],
        "ledger_entries": [{"id": "rent_01", "description": "Monthly Rent", "amount": 1500.0, "date_posted": "2026-02-01T00:00:00Z", "balance_running": 1500.0}],
        "notes": ["Tenant promised to pay next week."]
    }
    resp = client.post("/api/appfolio/sync-ledger", json=payload)
    if resp.status_code != 200:
        print(f"Server Error in Case 1: {resp.status_code} - {resp.text}")
        sys.exit(1)
        
    data = resp.json()
    assert data["brain_engine_result"]["action"] == "PROCEED", f"Failed Case 1: {data}"
    print("[PASS] Case 1: Standard Delinquency PROCEED")

    # CASE 2: Water Bill Only (< 5 days) -> HOLD
    payload = {
        "tenant_id": "tnt_water_1", "work_item_id": f"wi_{uuid.uuid4()}", "tenant_tags": [],
        "ledger_entries": [{"id": "water_01", "description": "Seattle Public Utilities - Water", "amount": 150.0, "date_posted": "2026-02-21T00:00:00Z", "balance_running": 150.0}],
        "notes": []
    }
    resp = client.post("/api/appfolio/sync-ledger", json=payload)
    if resp.status_code != 200:
         print(f"Error Case 2: {resp.text}")
         sys.exit(1)
    data = resp.json()
    if data.get("brain_engine_result", {}).get("action") == "PROCEED":
         print(f"FAILED Case 2. Payload returned: {data}")
         sys.exit(1)
    print("[PASS] Case 2: Water Bill Only HOLD")

    # CASE 3: DNC Tag Active -> HOLD
    payload = {
        "tenant_id": "tnt_dnc_1", "work_item_id": f"wi_{uuid.uuid4()}", "tenant_tags": ["VIP", "do not contact"], 
        "ledger_entries": [{"id": "rent_02", "description": "Rent", "amount": 5000.0, "date_posted": "2026-01-01T00:00:00Z", "balance_running": 5000.0}],
        "notes": []
    }
    resp = client.post("/api/appfolio/sync-ledger", json=payload)
    data = resp.json()
    assert data["brain_engine_result"]["action"] != "PROCEED", f"Failed Case 3: {data}"
    print("[PASS] Case 3: DNC Tag Active HOLD")

    # CASE 4: Sensitive State (Death/Sickness) -> HOLD
    payload = {
        "tenant_id": "tnt_death_1", "work_item_id": f"wi_{uuid.uuid4()}", "status": "delinquent", "tenant_tags": [],
        "ledger_entries": [{"id": "rent_03", "description": "Rent", "amount": 1000.0, "date_posted": "2026-02-01T00:00:00Z", "balance_running": 1000.0}],
        "notes": ["Tenant passed away last week, waiting on probate."]
    }
    resp = client.post("/api/appfolio/sync-ledger", json=payload)
    data = resp.json()
    assert data["brain_engine_result"]["action"] != "PROCEED", f"Failed Case 4: {data}"
    print("[PASS] Case 4: Sensitive Human State HOLD")
    
    print("\n--- ALL APPFOLIO ENGINE EDGE CASES VALIDATED ---")

if __name__ == "__main__":
    run_tests()
