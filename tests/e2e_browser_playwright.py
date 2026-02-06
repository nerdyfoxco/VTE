from playwright.sync_api import sync_playwright
import sys
import os

def run():
    print("Starting E2E Browser Verification...")
    try:
        with sync_playwright() as p:
            # Try launching chromium
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # --- STEP 1: Dashboard ---
            print("Step 1: Navigating to Dashboard...")
            try:
                page.goto("http://localhost:3000/dashboard", timeout=10000)
            except Exception as e:
                print(f"FAIL: Could not load dashboard. Is frontend running? {e}")
                sys.exit(1)

            # Verification 1: Header
            h1 = page.locator("h1").first.text_content()
            print(f"Found Header: {h1}")
            if "Kevin's Work Day" not in h1:
                print(f"FAIL: Header mismatch. Expected 'Kevin's Work Day'")
                sys.exit(1)
            
            # Verification 2: Button
            if page.locator("#btn_export_audit").count() == 0:
                 print("FAIL: 'Export Audit' button (btn_export_audit) missing!")
                 sys.exit(1)
                 
            # Screenshot
            cwd = os.getcwd()
            dash_path = os.path.join(cwd, "dashboard_verified.png")
            page.screenshot(path=dash_path)
            print(f"PASS: Dashboard UI Verified. Screenshot: {dash_path}")
            
            # --- STEP 2: Headless Surface ---
            print("Step 2: Navigating to Headless Surface...")
            page.goto("http://localhost:3000/agent/headless")
            
            # Verification 1: Status
            status = page.locator("#agent-status").text_content()
            if "READY" not in status:
                 print(f"FAIL: Agent status not READY")
                 sys.exit(1)
                 
            # Verification 2: Button
            if page.locator("#btn_export_audit").count() == 0:
                 print("FAIL: Headless 'Export Audit' button missing!")
                 sys.exit(1)

            # Screenshot
            head_path = os.path.join(cwd, "headless_verified.png")
            page.screenshot(path=head_path)
            print(f"PASS: Headless Surface Verified. Screenshot: {head_path}")
            
            browser.close()
            
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
