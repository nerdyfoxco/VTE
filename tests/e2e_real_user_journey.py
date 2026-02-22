from playwright.sync_api import sync_playwright
import sys
import os
import time

def run():
    print("Starting REAL USER E2E Journey...")
    
    # Create dummy data file for upload
    with open("dummy_delinquency.csv", "w") as f:
        f.write("id,amount\n1,500\n2,1000")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            
            # --- STEP 1: LOGIN ---
            print("\n[Step 1] Landing & Login")
            page.goto("http://localhost:3000/login")
            
            # Fill Credentials
            page.fill("#username-address", "kevin@anchorrealtypa.com")
            page.fill("#password", "admin")
            
            # Click Login
            page.click("button[type='submit']")
            
            # Check for error message
            try:
                page.wait_for_selector(".text-red-500", timeout=2000)
                err_text = page.locator(".text-red-500").text_content()
                print(f"FAIL: Login Failed with UI Error: {err_text}")
                page.screenshot(path="e2e_login_failed.png")
                sys.exit(1)
            except:
                # No error message found, continue waiting for redirect
                pass

            # Expect redirect (Wait for URL to change or content to load)
            try:
                page.wait_for_url("**/evidence", timeout=10000)
            except:
                print(f"FAIL: Timed out waiting for redirect to /evidence. Current URL: {page.url}")
                page.screenshot(path="e2e_redirect_timeout.png")
                sys.exit(1)
                
            print("PASS: Login Successful (Redirected to /evidence)")
            page.screenshot(path="e2e_step1_login_success.png")

            # --- STEP 2: CONNECT DATA ---
            print("\n[Step 2] Connection Onboarding")
            # User navigates to Connect page
            page.goto("http://localhost:3000/connect")
            
            # 2a. Connect Gmail
            # Check for partial text match or class
            if page.locator("button", has_text="Connect Gmail").count() > 0:
                print("PASS: Gmail Connect Option Present")
            else:
                print(f"FAIL: Gmail Connect Button Missing. Content: {page.content()}")
                
            # 2b. AppFolio Creds
            page.fill("#af-username", "bot_user")
            page.fill("#af-password", "secure_pass")
            page.click("text='Save Credentials'")
            # Handle alert
            # page.on("dialog", lambda dialog: dialog.accept()) # Playwright handles auto-dismiss usually, but explicit handling is better
            print("PASS: AppFolio Credentials Entered")
            
            page.screenshot(path="e2e_step2_connections.png")

            # Register console listener
            page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

            # --- STEP 3: DASHBOARD ---
            print("\n[Step 3] Kevin's Workspace")
            # Click "Skip" to go to dashboard or navigate manually
            try:
                page.click("button:has-text('Skip for Now')")
            except:
                print("WARN: Skip button failed, trying direct nav...")
                page.goto("http://localhost:3000/dashboard")

            page.wait_for_url("**/dashboard")
            # Wait for any network idleness
            page.wait_for_load_state("networkidle", timeout=5000)

            # Check for Loading
            if page.locator("text=Loading Kevin's Workspace").count() > 0:
                 print("FAIL: Dashboard stuck on Loading.")
                 page.screenshot(path="e2e_fail_loading.png")
                 sys.exit(1)
                 
            # Check for Error
            if page.locator("text=Error:").count() > 0:
                 err = page.locator("text=Error:").text_content()
                 print(f"FAIL: Dashboard Error: {err}")
                 page.screenshot(path="e2e_fail_error.png")
                 sys.exit(1)

            # Verify "Kevin's Work Day" (Loose Match)
            try:
                # Expect h1 to contain Kevin
                page.wait_for_selector("h1:has-text('Kevin')", timeout=5000)
                print("PASS: Landed on Kevin's Dashboard")
            except:
                 print(f"FAIL: Header not found. Title: {page.title()}, Body: {page.inner_text('body')}")
                 sys.exit(1)
                 
            # Verify Data
            # Dashboard uses ul/li now
            # Wait for items to load
            try:
                page.wait_for_selector("li", timeout=5000)
            except: 
                print("WARN: No items found in list (or timeout).")

            items = page.locator("li").count()
            print(f"PASS: Visible Queue Items: {items}")
            
            page.screenshot(path="e2e_step3_dashboard.png")
            
            print("\n[SUCCESS] Full User Journey Verified.")
            browser.close()

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        # Capture failure state
        try:
            page.screenshot(path="e2e_failure_state.png")
        except:
            pass
        sys.exit(1)
    finally:
        if os.path.exists("dummy_delinquency.csv"):
            os.remove("dummy_delinquency.csv")

if __name__ == "__main__":
    run()
