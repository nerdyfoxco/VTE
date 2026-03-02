
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def login():
    print("0. Logging in...")
    # Using dev defaults: user/admin
    payload = {"username": "user", "password": "admin"}
    try:
        r = requests.post(f"{BASE_URL}/auth/token", data=payload)
        if r.status_code == 200:
            token = r.json()["access_token"]
            print(f"   Success! Token: {token[:10]}...")
            return token
        else:
            print(f"   Login Failed: {r.text}")
            return None
    except Exception as e:
        print(f"   Login Error: {e}")
        return None

def test_flow():
    token = login()
    if not token:
        return
        
    headers = {"Authorization": f"Bearer {token}"}

    print("1. Health Check...")
    try:
        r = requests.get("http://localhost:8000/health")
        print(r.json())
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return

    print("\n2. Register Property (Dogfood Heights)...")
    payload = {
        "actor": {"user_id": "script_bot", "role": "system_bot"},
        "intent": {
            "action": "REGISTER_PROPERTY",
            "target_resource": "auto-gen",
            "parameters": {"name": "Dogfood Heights", "address": "123 Dogfood Ln"}
        },
        "evidence_hash": None,
        "outcome": "PROPOSED",
        "policy_version": "1.0"
    }
    r = requests.post(f"{BASE_URL}/decisions", json=payload, headers=headers)
    if r.status_code == 200:
        print("   Property Decision POSTED. Waiting for projection...")
    else:
        print(f"   Failed: {r.text}")
        return

    time.sleep(2)

    print("\n3. Verify Property Exists...")
    r = requests.get(f"{BASE_URL}/inventory/properties", headers=headers)
    props = r.json()
    dogfood_prop = next((p for p in props if p["name"] == "Dogfood Heights"), None)
    
    if dogfood_prop:
        print(f"   SUCCESS: Found {dogfood_prop['name']} (ID: {dogfood_prop['property_id']})")
    else:
        print("   FAILURE: Property not found in projection.")
        return

    print("\n4. Register Unit (Unit 101)...")
    # Note: Using the intent 'REGISTER_UNIT' which should exist in tasks.py
    # We need the property_id from step 3
    prop_id = dogfood_prop['property_id']
    
    payload_unit = {
        "actor": {"user_id": "script_bot", "role": "system_bot"},
        "intent": {
            "action": "REGISTER_UNIT",
            "target_resource": prop_id, # Target is the Property ID
            "parameters": {"name": "Unit 101", "status": "VACANT"}
        },
        "evidence_hash": None,
        "outcome": "PROPOSED",
        "policy_version": "1.0"
    }
    
    r = requests.post(f"{BASE_URL}/decisions", json=payload_unit)
    if r.status_code == 200:
        print("   Unit Decision POSTED. Waiting for projection...")
    else:
        print(f"   Failed: {r.text}")
        return

    time.sleep(2)

    print("\n5. Verify Unit Exists...")
    r = requests.get(f"{BASE_URL}/inventory/properties")
    props = r.json()
    updated_prop = next((p for p in props if p["property_id"] == prop_id), None)
    
    if updated_prop and len(updated_prop.get("units", [])) > 0:
        print(f"   SUCCESS: Found {len(updated_prop['units'])} units.")
        print(f"   Unit Details: {updated_prop['units']}")
    else:
        print("   FAILURE: Unit not found in projection.")

if __name__ == "__main__":
    test_flow()
