import requests
import sys

BASE_URL = "http://localhost:8000"

def get_valid_token():
    try:
        # User: admin / Admin@123456!
        payload = {
            "username": "admin",
            "password": "Admin@123456!"
        }
        r = requests.post(f"{BASE_URL}/api/v1/auth/token", data=payload)
        r.raise_for_status()
        return r.json()["access_token"]
    except Exception as e:
        print(f"FAILED to get token: {e}")
        sys.exit(1)
