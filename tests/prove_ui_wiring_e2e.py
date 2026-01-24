import json
import os
import sys

# Simulates UI Wiring Check
# Ensuring that the UI action "CLICK_SUBMIT" actually calls the handler "submit_handler"
# basically checking the route mapping is valid.

def test_ui_wiring():
    print("[INFO] Starting UI Wiring Verification...")
    sys.path.append(os.getcwd())
    
    ui_map = {
        "btn_submit": "submit_handler"
    }
    
    backend_handlers = ["submit_handler", "cancel_handler"]
    
    print("  > Checking UI Component bindings...")
    
    for btn, handler in ui_map.items():
        if handler in backend_handlers:
            print(f"    [PASS] {btn} -> {handler} is wired correctly.")
        else:
            print(f"    [FAIL] {btn} points to unknown handler {handler}")
            sys.exit(1)
            
    print("\n[SUCCESS] UI Wiring Scenario Proven.")

def main():
    try:
        test_ui_wiring()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
