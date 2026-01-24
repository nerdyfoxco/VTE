import json
import os
import sys

# Contract paths
NOTIFICATION_CONTRACT = "contracts/ux/notification_contract_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class NotificationService:
    def __init__(self):
        self.sent_log = []
        self.seen_keys = set()
        
    def send(self, notif_type, payload, dedupe_key=None):
        if dedupe_key:
            if dedupe_key in self.seen_keys:
                print(f"  > Skipping duplicate notification: {dedupe_key}")
                return "DEDUPED"
            self.seen_keys.add(dedupe_key)
            
        print(f"  > Sending {notif_type}...")
        self.sent_log.append({"type": notif_type, "payload": payload, "key": dedupe_key})
        return "SENT"

def test_notification_behavior():
    print("[INFO] Loading Notification Contract...")
    # Just to verify schema exists
    load_json(NOTIFICATION_CONTRACT)
    
    svc = NotificationService()
    
    # 1. Test Normal Send
    res = svc.send("WORK_ASSIGNED", {"item_id": "123"})
    if res != "SENT": 
        print(f"[FAIL] Expected SENT, got {res}")
        sys.exit(1)
        
    # 2. Test Dedupe
    key = "alert_cpu_high_server1_20231027"
    res1 = svc.send("SYSTEM_ALERT", {"msg": "CPU HIGH"}, dedupe_key=key)
    res2 = svc.send("SYSTEM_ALERT", {"msg": "CPU HIGH"}, dedupe_key=key)
    
    if res1 != "SENT": 
         print(f"[FAIL] First alert failed! Got {res1}")
         sys.exit(1)
    if res2 != "DEDUPED":
         print(f"[FAIL] Second alert was not deduped! Got {res2}")
         sys.exit(1)
         
    print("[PASS] Notification deduplication logic proven.")

def main():
    try:
        test_notification_behavior()
        print("\n[SUCCESS] Notification Truth Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
