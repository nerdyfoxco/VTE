from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Login First
        print("Navigating to Login...")
        page.goto("http://localhost:3001/login")
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "Admin@123456!")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard")
        print("Logged in.")

        # Intercept to force error
        print("Forcing Error...")
        def handle_error(route):
            print("Intercepting request -> returning 500")
            route.fulfill(status=500, body="Internal Server Error")

        page.route("**/api/v1/queue*", handle_error)
        page.reload()

        # Check for Error UI
        print("Checking for Error UI...")
        try:
            page.wait_for_selector("text=Something went wrong", timeout=5000)
            page.screenshot(path="error_state_success.png")
            print("SUCCESS: Error State UI found.")
        except Exception as e:
            print(f"FAILURE: Error State not found. {e}")
            page.screenshot(path="error_state_failure.png")
        
        # Test Retry (Remove intercept and click retry)
        print("Testing Retry...")
        page.unroute("**/api/v1/queue*") # Clear intercept
        
        page.click("button:has-text('Try Again')")
        
        # Should load items now
        try:
            page.wait_for_selector("text=Kevin's Work Day", timeout=5000)
             # Wait for a list item
            page.wait_for_selector("text=Priority:", timeout=5000)
            page.screenshot(path="retry_success.png")
            print("SUCCESS: Retry worked, items loaded.")
        except Exception as e:
            print(f"FAILURE: Retry failed. {e}")
            page.screenshot(path="retry_failure.png")

        browser.close()

if __name__ == "__main__":
    run()
