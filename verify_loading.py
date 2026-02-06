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

        # Reload dashboard to trigger loading state again
        # Intercept requests to delay response so we can see loading state
        def handle_route(route):
            time.sleep(2) # Delay 2s
            route.continue_()

        page.route("**/api/v1/queue*", handle_route)
        
        print("Reloading Dashboard...")
        page.reload()

        # Check for skeleton immediately
        print("Checking for Skeleton...")
        try:
            skeleton = page.wait_for_selector(".animate-pulse", timeout=5000)
            if skeleton:
                print("SUCCESS: Skeleton loader found.")
                page.screenshot(path="loading_skeleton.png")
                print("Captured loading_skeleton.png")
            else:
                print("FAILURE: Skeleton loader not found.")
                page.screenshot(path="failure_loading.png")
        except Exception as e:
            print(f"Error waiting for skeleton: {e}")
            page.screenshot(path="error_loading.png")

        browser.close()

if __name__ == "__main__":
    run()
