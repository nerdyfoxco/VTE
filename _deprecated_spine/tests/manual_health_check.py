from fastapi.testclient import TestClient
from vte.main import app
import sys

# Initialize TestClient
client = TestClient(app)

print("Testing /health endpoint...")
try:
    response = client.get("/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200 and response.json().get("database") == "connected":
        print("SUCCESS: API and DB are healthy.")
        sys.exit(0)
    else:
        print("FAILURE: Health check returned unexpected status.")
        sys.exit(1)
except Exception as e:
    print(f"FAILURE: Exception during request: {e}")
    sys.exit(1)
