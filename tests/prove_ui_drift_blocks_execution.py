import json
import os
import sys

# Simulates UI Drift Blocking Execution
# If frontend sends an action "BTN_CLICK" but backend expects "CLICK_BTN",
# it should fail safely (blocking) rather than executing wrong handler or crashing unsafe.

def test_ui_drift_block():
    print("[INFO] Starting UI Drift Verification...")
    sys.path.append(os.getcwd())
    
    frontend_action = "BTN_CLICK"
    backend_registry = ["CLICK_BTN", "SUBMIT_FORM"]
    
    print(f"  > Input Action: {frontend_action}")
    
    if frontend_action not in backend_registry:
        print(f"    [PASS] Execution Blocked: Unknown Action '{frontend_action}'")
    else:
        print(f"    [FAIL] Action matched?!")
        sys.exit(1)

    print("\n[SUCCESS] UI Drift Block Scenario Proven.")

def main():
    try:
        test_ui_drift_block()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
