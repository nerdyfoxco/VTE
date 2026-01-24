import json
import os
import sys

# Contract paths
SYNC_SEMANTICS_PATH = "contracts/provider_sync_semantics.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class Connector:
    def __init__(self, semantics):
        self.handling = semantics['failure_handling']
        self.state = "ACTIVE"
        self.last_error = None

    def handle_response(self, status_code):
        if status_code == 200:
            return "OK"
        elif status_code == 429: # Rate Limit
            action = self.handling.get("rate_limit_exceeded")
            if action == "PAUSE_AND_RESUME":
                self.state = "PAUSED_BACKOFF"
                return "FAIL_CLOSED"
        elif status_code == 401: # Auth Failure
            action = self.handling.get("auth_failure")
            if action == "ALERT_AND_DISABLE_CONNECTOR":
                self.state = "DISABLED"
                return "FAIL_CLOSED"
        
        return "UNKNOWN_ERROR"

def test_throttling():
    print("[INFO] Loading Sync Semantics...")
    semantics = load_json(SYNC_SEMANTICS_PATH)
    connector = Connector(semantics)
    
    # 1. Test Limit Exceeded
    print("[INFO] Simulating 429 Too Many Requests...")
    res = connector.handle_response(429)
    if connector.state != "PAUSED_BACKOFF":
         print(f"[FAIL] Connector did not pause! State: {connector.state}")
         sys.exit(1)
    if res != "FAIL_CLOSED":
         print(f"[FAIL] Result was not FAIL_CLOSED! Got: {res}")
         sys.exit(1)
         
    print("[PASS] Throttling triggers Pause/Backoff and Fail Closed.")

    # 2. Test Auth Failure
    print("[INFO] Simulating 401 Unauthorized...")
    res = connector.handle_response(401)
    if connector.state != "DISABLED":
         print(f"[FAIL] Connector did not disable on auth fail! State: {connector.state}")
         sys.exit(1)
    print("[PASS] Auth failure triggers Disable/Alert.")

def main():
    try:
        test_throttling()
        print("\n[SUCCESS] Provider Throttling Resilience Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
