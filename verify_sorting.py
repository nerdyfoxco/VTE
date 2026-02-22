import requests
from datetime import datetime
from test_utils import get_valid_token

BASE_URL = "http://localhost:8000/api/v1/queue"
TOKEN = get_valid_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def verify_sorting():
    print("Verifying Sorting Logic...")
    
    # 1. Priority ASC
    print("\n[Priority ASC]")
    r = requests.get(f"{BASE_URL}?limit=5&sort_by=priority&order=asc", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    priorities = [i['priority'] for i in items]
    print(f"Priorities: {priorities}")
    if priorities == sorted(priorities):
        print("SUCCESS: Priority ASC verified.")
    else:
        print("FAILURE: Priority ASC mismatch.")

    # 2. Priority DESC
    print("\n[Priority DESC]")
    r = requests.get(f"{BASE_URL}?limit=5&sort_by=priority&order=desc", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    priorities = [i['priority'] for i in items]
    print(f"Priorities: {priorities}")
    if priorities == sorted(priorities, reverse=True):
        print("SUCCESS: Priority DESC verified.")
    else:
        print("FAILURE: Priority DESC mismatch.")

    # 3. Due Date ASC
    print("\n[Due Date ASC]")
    r = requests.get(f"{BASE_URL}?limit=5&sort_by=sla_deadline&order=asc", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    dates = [i['sla_deadline'] for i in items]
    print(f"Dates: {dates}")
    if dates == sorted(dates):
        print("SUCCESS: Due Date ASC verified.")
    else:
        print("FAILURE: Due Date ASC mismatch.")

if __name__ == "__main__":
    verify_sorting()
