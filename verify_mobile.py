from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile Context
        context = browser.new_context(viewport={"width": 375, "height": 667})
        page = context.new_page()

        # Login First
        print("Navigating to Login on Mobile...")
        page.goto("http://localhost:3001/login")
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "Admin@123456!")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard")
        print("Logged in.")

        # Check for Table (Should be hidden or not present)
        # Note: 'hidden sm:block' uses display:none. Playwright's .is_visible() respects this.
        # However, the element is still in DOM.
        print("Checking visibility...")
        
        # We look for the Table container's class to verify it has 'hidden'
        desktop_view = page.locator(".hidden.sm\\:block")
        
        # In Playwright, is_visible() returns False if display:none.
        if not desktop_view.is_visible():
            print("SUCCESS: Desktop Table hidden on Mobile.")
        else:
            print("FAILURE: Desktop Table is visible on Mobile.")

        # Check for Mobile Cards
        # We look for the Mobile container's class 'block sm:hidden'
        mobile_view = page.locator(".block.sm\\:hidden")
        
        if mobile_view.is_visible():
            print("SUCCESS: Mobile Cards container visible.")
            # Check for actual cards
            # Wait for content
            try:
                page.wait_for_selector("text=Priority:", timeout=5000)
                page.screenshot(path="mobile_layout_success.png")
                print("SUCCESS: Mobile content verified.")
            except:
                print("WARNING: No items found or cards not rendered yet.")
        else:
            print("FAILURE: Mobile Cards container hidden.")
            page.screenshot(path="mobile_layout_failure.png")

        browser.close()

if __name__ == "__main__":
    run()
