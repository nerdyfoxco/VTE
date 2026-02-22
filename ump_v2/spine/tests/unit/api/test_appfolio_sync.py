import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

base_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(base_dir / "src"))

from main import app

client = TestClient(app)

def test_appfolio_standard_delinquency_proceed():
    """
    Case 1: Ledger only contains normal rent delays. No sensitive constraints.
    Expected: Brain outputs PROCEED -> KevinOutreach dispatched.
    """
    payload = {
        "tenant_id": "tnt_standard_1",
        "work_item_id": "wi_001",
        "tenant_name": "Standard Kevin",
        "status": "delinquent",
        "tenant_tags": ["pet owner", "renters insurance"],
        "ledger_entries": [
            {"id": "rent_01", "description": "Monthly Rent", "amount": 1500.0, "date_posted": "2026-02-01T00:00:00Z", "balance_running": 1500.0}
        ],
        "notes": ["Tenant promised to pay next week."]
    }
    
    resp = client.post("/api/appfolio/sync-ledger", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["brain_engine_result"]["action"] == "PROCEED"
    assert "status': 'SENT'" in str(data["hands_execution_result"])

def test_appfolio_water_bill_only_hold():
    """
    Case 2: The only balance owed is a Water bill under 5 days old.
    Expected: Brain outputs HOLD. Hands execution is skipped.
    """
    payload = {
        "tenant_id": "tnt_water_1",
        "work_item_id": "wi_002",
        "tenant_tags": [],
        "ledger_entries": [
            {"id": "water_01", "description": "Seattle Public Utilities - Water", "amount": 150.0, "date_posted": "2026-02-21T00:00:00Z", "balance_running": 150.0}
        ],
        "notes": []
    }
    
    resp = client.post("/api/appfolio/sync-ledger", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["brain_engine_result"]["action"] == "HOLD"
    assert "Skipped" in data["hands_execution_result"]

def test_appfolio_dnc_safety_guard():
    """
    Case 3: 'Do Not Contact' tag is active.
    Expected: Brain must output HOLD regardless of balance amount.
    """
    payload = {
        "tenant_id": "tnt_dnc_1",
        "work_item_id": "wi_003",
        "tenant_tags": ["VIP", "do not contact", "bankruptcy"], 
        "ledger_entries": [
            {"id": "rent_02", "description": "Rent", "amount": 5000.0, "date_posted": "2026-01-01T00:00:00Z", "balance_running": 5000.0}
        ],
        "notes": []
    }
    
    resp = client.post("/api/appfolio/sync-ledger", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["brain_engine_result"]["action"] == "HOLD"

def test_appfolio_sensitive_human_state():
    """
    Case 4: Context Checker identifies sensitive keywords in the notes.
    Expected: Brain must execute compassionate HOLD.
    """
    payload = {
        "tenant_id": "tnt_death_1",
        "work_item_id": "wi_004",
        "status": "delinquent",
        "tenant_tags": [],
        "ledger_entries": [
            {"id": "rent_03", "description": "Rent", "amount": 1000.0, "date_posted": "2026-02-01T00:00:00Z", "balance_running": 1000.0}
        ],
        "notes": ["Received call from daughter. Tenant passed away last week, waiting on probate."]
    }
    
    resp = client.post("/api/appfolio/sync-ledger", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["brain_engine_result"]["action"] == "HOLD"
