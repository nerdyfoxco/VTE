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
        # page.wait_for_url("**/dashboard") # Changed to login redirects to root
        page.wait_for_url("http://localhost:3001/")
        print("Logged in. Checking Breadcrumbs...")

        try:
            # Check for Breadcrumb navigation element
            page.wait_for_selector("nav[aria-label='Breadcrumb']", timeout=5000)
            
            # Check for Home link
            home_link = page.locator("a[href='/']:has-text('Home')")
            if home_link.is_visible():
                print("SUCCESS: 'Home' link found.")
            else:
                raise Exception("Home link not found")

            # Check for Dashboard link
            dash_link = page.locator("a[href='/dashboard']:has-text('Dashboard')")
            if dash_link.is_visible():
                print("SUCCESS: 'Dashboard' link found.")
            else:
                raise Exception("Dashboard link not found")

            # Check for Current Page (text, not link)
            current_page = page.locator("span[aria-current='page']:has-text(\"Kevin's Work Day\")")
            if current_page.is_visible():
                print("SUCCESS: Current page text found.")
            else:
                raise Exception("Current page text not found")

            page.screenshot(path="breadcrumbs_success.png")
            print("SUCCESS: Breadcrumbs verified.")

        except Exception as e:
            print(f"FAILURE: Breadcrumbs missing or incorrect. {e}")
            page.screenshot(path="breadcrumbs_failure.png")

        browser.close()

if __name__ == "__main__":
    run()
