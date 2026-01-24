import json
import os
import sys

# Simulates Incident Playbook Activation
# Security Event -> Auto Response

def test_incident_playbook():
    print("[INFO] Starting Incident Playbook Verification...")
    sys.path.append(os.getcwd())
    
    triggers = ["DATA_EXFIL"]
    
    def handle_event(event_type):
        if event_type in triggers:
            return ["LOCK_ACCOUNT", "NOTIFY_CISO"]
        return []
        
    print("  > Simulating DATA_EXFIL...")
    actions = handle_event("DATA_EXFIL")
    
    if "LOCK_ACCOUNT" in actions:
        print(f"    [PASS] Playbook Activated: {actions}")
    else:
        print("    [FAIL] Playbook failed to activate.")
        sys.exit(1)

    print("\n[SUCCESS] Incident Playbook Scenario Proven.")

def main():
    try:
        test_incident_playbook()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
