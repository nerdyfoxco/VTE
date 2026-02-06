import requests

BASE_URL = "http://localhost:8000/api/v1/queue"
TOKEN = "fake-jwt-token-admin"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def verify_search():
    print("Verifying Search Logic...")
    
    # 1. Search: "Urgent"
    print("\n[Search: 'Urgent']")
    r = requests.get(f"{BASE_URL}?search=Urgent", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    titles = [i['title'] for i in items]
    print(f"Items found: {len(items)}")
    print(f"Titles: {titles}")
    
    if any("Urgent" in t for t in titles) and len(items) > 0:
        print("SUCCESS: 'Urgent' search verified.")
    else:
        print("FAILURE: 'Urgent' search mismatch.")

    # 2. Search: "Security"
    print("\n[Search: 'Security']")
    r = requests.get(f"{BASE_URL}?search=Security", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    titles = [i['title'] for i in items]
    print(f"Items found: {len(items)}")
    print(f"Titles: {titles}")
    if any("Security" in t for t in titles) and len(items) > 0:
        print("SUCCESS: 'Security' search verified.")
    else:
         print("FAILURE: 'Security' search mismatch.")

        
    # 3. Search: "Banana" (Non-existent)
    print("\n[Search: 'Banana']")
    r = requests.get(f"{BASE_URL}?search=Banana", headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    print(f"Items found: {len(items)}")
    if len(items) == 0:
         print("SUCCESS: Empty search verified.")
    else:
         print("FAILURE: 'Banana' should return 0 items.")

if __name__ == "__main__":
    verify_search()
