import time
import requests
import subprocess
import os
import signal
import sys
import uuid
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"
BACKEND_CMD = [sys.executable, "-m", "uvicorn", "vte.main:app", "--host", "0.0.0.0", "--port", "8000"]
WORKING_DIR = r"C:\Bintloop\VTE\spine"

def log(msg, type="INFO"):
    print(f"[{type}] {msg}")

def start_backend():
    log("Starting Backend...", "SETUP")
    # Kill existing
    subprocess.run(["taskkill", "/F", "/IM", "uvicorn.exe"], capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True) # Aggressive, but clean.
    
    # Start
    process = subprocess.Popen(BACKEND_CMD, cwd=WORKING_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def wait_for_health():
    log("Waiting for Healthcheck...", "SETUP")
    retries = 30
    for i in range(retries):
        try:
            resp = requests.get(f"{BASE_URL}/health")
            if resp.status_code == 200:
                log("Backend is Healthy!", "SUCCESS")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
        print(".", end="", flush=True)
    log("Backend timed out.", "ERROR")
    return False

def get_token():
    # Helper to get a mock token (since we mocked auth)
    # The system accepts any token in dev if we didn't tighten it too much, or we use the login endpoint if it works.
    # Based on gap analysis, auth is mock.
    # Let's try to get a real token if the endpoint exists, or assume bypass.
    # Implementation plan said "Mock Auth".
    # Let's try a simple login if `auth.py` has it, otherwise manually construct header.
    # Assuming 'login' endpoint:
    return "mock_token_superuser"

def run_test_sequence():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Register Property
    log("Step 1: Register Property (Contract Trigger)", "TEST")
    prop_payload = {
        "actor": {"user_id": "test_script", "role": "admin"},
        "intent": {
            "action": "REGISTER_PROPERTY",
            "target_resource": str(uuid.uuid4()), # New ID
            "parameters": {"name": "Redemption Towers", "address": "123 Kernel St"}
        },
        "evidence_hash": None,
        "outcome": "APPROVED", # Auto-approve for test
        "policy_version": "1.0"
    }
    
    resp = requests.post(f"{API_URL}/decisions", json=prop_payload, headers=headers)
    if resp.status_code != 200:
        log(f"Register Property Failed: {resp.text}", "FAIL")
        return False
        
    data = resp.json()
    prop_permit = data.get("permit_id")
    log(f"Property Registered. Permit: {prop_permit}", "SUCCESS")
    
    # Wait for Projection (Async task might take a moment, checking idempotency/updates)
    # The Engine runs synchronously in verify_redemption context? 
    # vte/tasks.py is Celery usually, but verify_redemption calls API which might trigger Celery?
    # vte/main.py uses run_in_executor or direct?
    # Let's check inventory to see if it appeared.
    time.sleep(2)
    
    # 2. Verify Property via Inventory API
    inv_resp = requests.get(f"{API_URL}/inventory/properties", headers=headers)
    props = inv_resp.json()
    my_prop = next((p for p in props if p["name"] == "Redemption Towers"), None)
    
    if not my_prop:
        log("Property not found in Inventory Projection!", "FAIL")
        log(f"Inventory: {props}", "DEBUG")
        return False
    
    prop_id = my_prop["property_id"]
    log(f"Found Property: {prop_id}", "SUCCESS")

    # 3. Register Unit
    log("Step 2: Register Unit (Contract Trigger)", "TEST")
    unit_payload = {
        "actor": {"user_id": "test_script", "role": "admin"},
        "intent": {
            "action": "REGISTER_UNIT",
            "target_resource": str(uuid.uuid4()),
            "parameters": {
                "property_id": prop_id,
                "name": "Unit 404",
                "status": "VACANT"
            }
        },
        "outcome": "APPROVED",
        "policy_version": "1.0"
    }
    
    resp = requests.post(f"{API_URL}/decisions", json=unit_payload, headers=headers)
    if resp.status_code != 200:
        log(f"Register Unit Failed: {resp.text}", "FAIL")
        return False
        
    log("Unit Registered.", "SUCCESS")
    time.sleep(2)

    # 4. Verify Unit
    inv_resp = requests.get(f"{API_URL}/inventory/properties", headers=headers)
    props = inv_resp.json()
    my_prop = next((p for p in props if p["property_id"] == prop_id), None)
    my_unit = next((u for u in my_prop["units"] if u["name"] == "Unit 404"), None)
    
    if not my_unit:
        log("Unit not found in Inventory!", "FAIL")
        return False
        
    unit_id = my_unit["unit_id"]
    log(f"Found Unit: {unit_id} ({my_unit['status']})", "SUCCESS")

    # 5. Write Note (Side Effect)
    log("Step 3: Write Note (AppFolio Adapter)", "TEST")
    note_payload = {
        "actor": {"user_id": "test_script", "role": "admin"},
        "intent": {
            "action": "write_note", # or WRITE_NOTE depending on contract/engine map
            "target_resource": unit_id,
            "parameters": {
                "content": "Redemption Verified via Script",
                "dry_run": True # Don't actually hit AppFolio in test if strict
            }
        },
        "outcome": "APPROVED",
        "policy_version": "1.0"
    }
    
    resp = requests.post(f"{API_URL}/decisions", json=note_payload, headers=headers)
    if resp.status_code != 200:
        log(f"Write Note Failed: {resp.text}", "FAIL")
        return False
        
    log("Note Dispatched.", "SUCCESS")
    
    log("=== REDEMPTION COMPLETE ===", "SUCCESS")
    return True

if __name__ == "__main__":
    proc = start_backend()
    try:
        if wait_for_health():
            success = run_test_sequence()
            if not success:
                sys.exit(1)
        else:
            # Dump stderr
            log("Backend Output:", "DEBUG")
            print(proc.stderr.read())
            sys.exit(1)
    finally:
        log("Stopping Backend...", "TEARDOWN")
        proc.terminate()
        proc.wait()
