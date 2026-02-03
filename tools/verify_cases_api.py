import requests
import sys
import json
import time

BASE_URL = "http://localhost:8003"
EMAIL = "testuser@example.com"
PASSWORD = "password123"

def print_step(msg):
    print(f"\n[STEP] {msg}")

def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)

def verify_cases_api():
    print("Starting Headless Case Lifecycle Verification...")

    # 1. Authenticate
    print_step("Authenticating...")
    auth_payload = {"email": EMAIL, "password": PASSWORD}
    try:
        res = requests.post(f"{BASE_URL}/auth/login", json=auth_payload)
        res.raise_for_status()
        token = res.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": "tenant-123" # Required by TenantContextMiddleware
        }
        print(f"  > Token acquired: {token[:10]}...")
    except Exception as e:
        fail(f"Login failed: {e}")

    # 2. Create Case
    print_step("Creating Case...")
    case_payload = {
        "title": "Headless Verification Case",
        "description": "Created by verify_cases_api.py",
        "tenant_id": "tenant-123" # Assuming admin can set this, or it's ignored/inferred
    }
    
    # Needs Idempotency Key generally, but let's see if plain POST works based on router
    headers["Idempotency-Key"] = f"idemp-{int(time.time())}"
    
    try:
        res = requests.post(f"{BASE_URL}/api/cases/", json=case_payload, headers=headers)
        if res.status_code == 422:
            print(res.json())
        res.raise_for_status()
        case = res.json()
        case_id = case["id"]
        print(f"  > Case Created: {case_id} [{case['status']}]")
    except Exception as e:
        fail(f"Create Case failed: {e}")

    # 3. List Cases
    print_step("Listing Cases...")
    try:
        res = requests.get(f"{BASE_URL}/api/cases/", headers=headers)
        res.raise_for_status()
        cases = res.json()
        print(f"  > Found {len(cases)} cases.")
        found = any(c["id"] == case_id for c in cases)
        if not found:
            fail("Created case not found in list!")
    except Exception as e:
        fail(f"List Cases failed: {e}")

    # 4. Get Case Detail
    print_step("Getting Case Detail...")
    try:
        res = requests.get(f"{BASE_URL}/api/cases/{case_id}", headers=headers)
        res.raise_for_status()
        detail = res.json()
        if detail["id"] != case_id:
             fail("ID mismatch in detail view")
        print("  > Detail OK")
    except Exception as e:
        fail(f"Get Case failed: {e}")

    # 5. State Machine: OPEN -> IN_PROGRESS
    print_step("Transition: OPEN -> IN_PROGRESS")
    try:
        res = requests.patch(f"{BASE_URL}/api/cases/{case_id}/status", json={"status": "IN_PROGRESS"}, headers=headers)
        res.raise_for_status()
        if res.json()["status"] != "IN_PROGRESS":
            fail("Status did not update to IN_PROGRESS")
        print("  > Transition OK")
    except Exception as e:
        fail(f"Transition failed: {e}")

    # 6. Invalid Transition: IN_PROGRESS -> OPEN (Depending on rules, usually allowed, let's try IN_PROGRESS -> CLOSED directly if allowed? Or something typically strictly forbidden like CLOSED -> OPEN?)
    # Actually, VTE rules: OPEN->IN_PROGRESS->RESOLVED->CLOSED. 
    # Let's try IN_PROGRESS -> CLOSED (might be skipped step, but maybe allowed? Let's check router logic if we can, but testing via API is better)
    # Let's try to set to some garbage status first to verify validation
    print_step("Invalid Status Value (GARBAGE)...")
    try:
        res = requests.patch(f"{BASE_URL}/api/cases/{case_id}/status", json={"status": "GARBAGE"}, headers=headers)
        if res.status_code == 422:
            print("  > Caught expected 422 for garbage status.")
        else:
            fail(f"Expected 422 for garbage, got {res.status_code}")
    except Exception:
        pass # Requests might raise for 422? No, confirm. requests.post doesn't raise unless raise_for_status called.

    # 7. Transition: IN_PROGRESS -> RESOLVED
    print_step("Transition: IN_PROGRESS -> RESOLVED")
    try:
        res = requests.patch(f"{BASE_URL}/api/cases/{case_id}/status", json={"status": "RESOLVED"}, headers=headers)
        res.raise_for_status()
        print("  > Transition OK")
    except Exception as e:
         fail(f"Transition failed: {e}")

    # 8. Transition: RESOLVED -> CLOSED
    print_step("Transition: RESOLVED -> CLOSED")
    try:
        res = requests.patch(f"{BASE_URL}/api/cases/{case_id}/status", json={"status": "CLOSED"}, headers=headers)
        res.raise_for_status()
        print("  > Transition OK")
    except Exception as e:
         fail(f"Transition failed: {e}")

    # 9. Verify Final State
    res = requests.get(f"{BASE_URL}/api/cases/{case_id}", headers=headers)
    if res.json()["status"] == "CLOSED":
        print("\n[SUCCESS] All Case Lifecycle Headless Tests Passed.")
    else:
        fail("Final state check failed.")

if __name__ == "__main__":
    verify_cases_api()
