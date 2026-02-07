import requests
import datetime
from test_utils import get_valid_token

BASE_URL = "http://localhost:8000/api/v1/decisions"
TOKEN = get_valid_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def seed():
    print("Seeding data...")
    # Create 15 items with mixed priorities and names
    items = [
        ("High Priority Task A", "PROPOSED", 1),
        ("Low Priority Task B", "PROPOSED", 3),
        ("Medium Priority Task C", "PROPOSED", 2),
        ("Urgent Request D", "PROPOSED", 1),
        ("Routine Check E", "PROPOSED", 3),
        ("Completed Task F", "APPROVED", 1),
        ("Review Doc G", "PROPOSED", 2),
        ("Audit Log H", "PROPOSED", 3),
        ("High Priority I", "PROPOSED", 1),
        ("Task J", "PROPOSED", 2),
        ("Task K", "PROPOSED", 3),
        ("Task L", "PROPOSED", 1),
        ("Task M", "PROPOSED", 2),
        ("Task N", "PROPOSED", 3),
        ("Task O", "PROPOSED", 1),
    ]

    for title, outcome, prio in items:
        payload = {
            "actor": {
                "user_id": "seed-user", 
                "role": "admin", 
                "session_id": "seed-session"
            },
            "intent": {
                "action": title,
                "target_resource": "db/seed",
                "parameters": {}
            },
            "evidence_hash": "seed-evidence-hash",
            "outcome": outcome,
            "policy_version": "v1.0"
        }
        # Note: Priority is mocked in get_unified_queue based on Title string (High/Low)
        # In routes.py: if "High" in intent_action: prio = 1 ...
        
        try:
            r = requests.post(BASE_URL, json=payload, headers=HEADERS)
            r.raise_for_status()
            print(f"Created: {title}")
        except Exception as e:
            print(f"Failed to create {title}: {e}")

if __name__ == "__main__":
    seed()
