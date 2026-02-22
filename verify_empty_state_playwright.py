from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to Login...")
        page.goto("http://localhost:3001/login")
        
        print("Logging in...")
        page.fill("input[id='username-address']", "admin")
        page.fill("input[id='password']", "Admin@123456!")
        page.click("button[type='submit']")
        
        print("Waiting for Dashboard...")
        page.wait_for_url("http://localhost:3001/")
        page.wait_for_selector("text=Kevin's Work Day")
        
        # Verify Search Input
        print("Finding Search Input...")
        search_input = page.wait_for_selector("input[placeholder='Search by Title...']")
        
        # Test Empty State
        print("Testing Empty State...")
        search_input.fill("NON_EXISTENT_XYZ")
        # Trigger change event just in case
        page.evaluate("document.querySelector(\"input[placeholder='Search by Title...']\").dispatchEvent(new Event('input', { bubbles: true }));")
        
        time.sleep(2) # Wait for debounce/fetch
        
        # Verify "No items found"
        page.wait_for_selector("text=No items found")
        page.screenshot(path="empty_state_success_headless.png")
        print("Captured empty_state_success_headless.png")
        
        # Clear Filters
        print("Clearing Filters...")
        page.click("button:has-text('Clear Filters')")
        
        time.sleep(2) # Wait for reload
        
        # Verify items returned
        page.wait_for_selector("text=Priority: P1", timeout=5000)
        page.screenshot(path="restored_state_success_headless.png")
        print("Captured restored_state_success_headless.png")
        
        browser.close()

if __name__ == "__main__":
    run()
