import requests
import json

BASE_URL = "http://localhost:8000/api/v1/queue"
TOKEN = "fake-jwt-token-admin"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def verify_pagination():
    try:
        # Page 1
        print("Fetching Page 1 (limit=5)...")
        r1 = requests.get(f"{BASE_URL}?skip=0&limit=5", headers=HEADERS)
        r1.raise_for_status()
        page1 = r1.json()
        print(f"Page 1 Items: {len(page1)}")
        ids1 = [item['id'] for item in page1]
        print(f"Page 1 IDs: {ids1}")

        # Page 2
        print("\nFetching Page 2 (skip=5, limit=5)...")
        r2 = requests.get(f"{BASE_URL}?skip=5&limit=5", headers=HEADERS)
        r2.raise_for_status()
        page2 = r2.json()
        print(f"Page 2 Items: {len(page2)}")
        ids2 = [item['id'] for item in page2]
        print(f"Page 2 IDs: {ids2}")

        # Verification
        intersection = set(ids1).intersection(set(ids2))
        if not intersection and len(page1) == 5 and len(page2) > 0:
            print("\nSUCCESS: Pagination logic verified. No overlap between pages.")
        else:
            print(f"\nFAILURE: Overlap found: {intersection} or incorrect counts.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_pagination()
