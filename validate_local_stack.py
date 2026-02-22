import requests
import time
import sys
import json

API_URL = "http://localhost:8000/api/v1"
HEALTH_URL = "http://localhost:8000/health"

def wait_for_health():
    print(f"Waiting for API at {HEALTH_URL}...")
    for i in range(30):
        try:
            resp = requests.get(HEALTH_URL, timeout=5)
            if resp.status_code == 200:
                print("API is Healthy!")
                return True
        except Exception as e:
            if i % 5 == 0:
                print(f"Waiting... ({e})")
        time.sleep(2)
    return False

def run_validation():
    print("\n--- VTE Local E2E Validation ---")
    
    # 1. Health
    if not wait_for_health():
        print("CRITICAL: API did not come up. Please run 'docker-compose up -d' first.")
        sys.exit(1)
        
    # 2. Trigger Ingestion (via new Endpoint)
    print("\n[1] Triggering Ingestion Agent...")
    try:
        resp = requests.post(f"{API_URL}/agents/ingest")
        print(f"Status: {resp.status_code}, Body: {resp.json()}")
        if resp.status_code != 202:
            print("Failed to trigger ingestion.")
            sys.exit(1)
    except Exception as e:
        print(f"Error triggering ingestion: {e}")
        sys.exit(1)
        
    print("Ingestion Triggered. (Agent is running in background)")

    # 3. Create PROPOSED Decision (Manual Governance)
    print("\n[2] Creating PROPOSED Decision (Manual Governance)...")
    decision_payload = {
        "actor": {"user_id": "test_user", "role": "admin", "session_id": "test_sess"},
        "intent": {
            "action": "write_note",
            "target_resource": "101",
            "parameters": {"content": "E2E Verified by Local Script", "dry_run": True}
        },
        "evidence_hash": "dummy_hash_for_test",
        "outcome": "PROPOSED",
        "policy_version": "v1.0"
    }
    
    try:
        resp = requests.post(f"{API_URL}/decisions", json=decision_payload)
        if resp.status_code != 201:
            print(f"Failed to create decision: {resp.text}")
            sys.exit(1)
        
        decision_id = resp.json()["decision_id"]
        print(f"Created Decision: {decision_id}")
    except Exception as e:
        print(f"Connection Error: {e}")
        sys.exit(1)
    
    # 4. Approve Decision (Trigger Execution)
    print("\n[3] Approving Decision (Trigger Execution)...")
    approval_payload = decision_payload.copy()
    approval_payload["outcome"] = "APPROVED"
    
    resp = requests.post(f"{API_URL}/decisions", json=approval_payload)
    if resp.status_code != 201:
        print(f"Failed to approve: {resp.text}")
        sys.exit(1)
    
    print("Decision Approved. Execution Task Enqueued.")
    print("\n--- VALIDATION SUCCESSFUL ---")
    print("run 'docker-compose logs -f spine-worker' to watch the Visual Agent perform the writeback.")

if __name__ == "__main__":
    run_validation()
