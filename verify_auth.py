from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to Login...")
        page.goto("http://localhost:3001/login")
        
        # Verify Login UI
        try:
            page.wait_for_selector("input[name='username']", timeout=5000)
            print("SUCCESS: Login Form visible.")
        except:
            print("FAILURE: Login Form not visible.")
            page.screenshot(path="auth_failure_form.png")
            return

        # Perform Login
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "Admin@123456!")
        page.click("button[type='submit']")
        
        # Wait for redirect
        try:
            # Dashboard is at root
            # Relaxed check: Wait for navigation away from login
            page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
            print(f"Navigated to: {page.url}")
            print("SUCCESS: Redirected to Dashboard.")
            
            # Check for Token in LocalStorage
            token = page.evaluate("localStorage.getItem('access_token')")
            if token:
                 print("SUCCESS: Access Token found in LocalStorage.")
            else:
                 print("FAILURE: No Access Token in LocalStorage.")
                 
            page.screenshot(path="auth_success.png")
            
        except Exception as e:
            print(f"FAILURE: Login failed or redirect timed out. {e}")
            page.screenshot(path="auth_failure_redirect.png")

        browser.close()

if __name__ == "__main__":
    run()
