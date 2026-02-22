from fastapi.testclient import TestClient
from vte.main import app
import sys

client = TestClient(app)

print("1. Creating Evidence Bundle...")
evidence_payload = {
    "normalization_schema": "plaid_txn_v1",
    "items": [
        {
            "source": "plaid",
            "type": "txn_row",
            "data": {"amount": 500, "merchant": "Acme Corp"},
            "sha256": "dummy_sha_of_data"
        }
    ]
}

evidence_hash = None

try:
    resp = client.post("/api/v1/evidence", json=evidence_payload)
    print(f"Evidence Status: {resp.status_code}")
    if resp.status_code == 201:
        data = resp.json()
        evidence_hash = data["bundle_hash"]
        print(f"Created Bundle Hash: {evidence_hash}")
    else:
        print(f"Evidence Creation Failed: {resp.text}")
        sys.exit(1)
except Exception as e:
    print(f"Evidence Exception: {e}")
    sys.exit(1)

print("\n2. Creating Decision using Evidence Hash...")

payload = {
  "actor": {
    "user_id": "user_123",
    "role": "user",
    "session_id": "sess_abc"
  },
  "intent": {
    "action": "submit_claim",
    "target_resource": "claim_555",
    "parameters": {"amount": 500}
  },
  "evidence_hash": evidence_hash,
  "outcome": "APPROVED",
  "policy_version": "v1.0"
}

try:
    response = client.post("/api/v1/decisions", json=payload)
    print(f"Decision Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        data = response.json()
        if "decision_hash" in data and "decision_id" in data:
            print("SUCCESS: Decision created, hashed, and linked to evidence.")
            print(f"Hash: {data['decision_hash']}")
            print(f"Previous Hash: {data['previous_hash']}")
            sys.exit(0)
    
    print("FAILURE: Decision Creation failed.")
    sys.exit(1)

except Exception as e:
    print(f"FAILURE: Exception: {e}")
    sys.exit(1)
