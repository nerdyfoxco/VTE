import requests

BASE_URL = "http://localhost:8000/api/v1/queue"
TOKEN = "fake-jwt-token-admin"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def verify_filtering():
    print("Verifying Filtering Logic...")
    
    # 1. Status: COMPLETED
    print("\n[Filter: COMPLETED]")
    r = requests.get(f"{BASE_URL}?status=COMPLETED", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    statuses = [i['status'] for i in items]
    print(f"Items found: {len(items)}")
    print(f"Statuses: {set(statuses)}")
    
    if all(s == "COMPLETED" for s in statuses) and len(items) > 0:
        print("SUCCESS: COMPLETED filter verified.")
    else:
        print("FAILURE: COMPLETED filter mismatch or empty.")

    # 2. Status: PENDING (Default)
    print("\n[Filter: PENDING]")
    r = requests.get(f"{BASE_URL}?status=PENDING", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    statuses = [i['status'] for i in items]
    print(f"Items found: {len(items)}")
    if all(s == "PENDING" for s in statuses) and len(items) > 0:
        print("SUCCESS: PENDING filter verified.")
    else:
        print("FAILURE: PENDING filter mismatch.")

    # 3. Priority: 1
    print("\n[Filter: Priority 1]")
    r = requests.get(f"{BASE_URL}?priority=1", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    priorities = [i['priority'] for i in items]
    print(f"Priorities: {set(priorities)}")
    if all(p == 1 for p in priorities) and len(items) > 0:
         print("SUCCESS: Priority 1 filter verified.")
    else:
         print("FAILURE: Priority 1 filter mismatch.")

if __name__ == "__main__":
    verify_filtering()
