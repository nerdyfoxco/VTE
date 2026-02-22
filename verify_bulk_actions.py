import time
from playwright.sync_api import sync_playwright
import sys

def verify_bulk_actions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("Navigating to Login...")
            page.goto("http://localhost:3001/login")
            
            print("Logging in...")
            page.fill("input[type='text']", "admin")
            page.fill("input[type='password']", "admin")
            page.click("button[type='submit']")
            
            print("Waiting for Dashboard...")
            page.wait_for_url(lambda u: "/login" not in u)
            page.wait_for_selector("text=Showing", timeout=10000)
            
            # 1. Locate Select All
            # Ensure items are visible first
            print("Checking if items are visible...")
            try:
                page.wait_for_selector("input[name='select-all']", timeout=5000)
            except:
                print("Select All not found. Checking for 'No items found'...")
                if page.is_visible("text=No items found"):
                    print("No items found. Clicking 'Clear Filters'...")
                    page.click("text=Clear Filters")
                    page.wait_for_selector("input[name='select-all']", timeout=10000)
                else:
                    print("FAILURE: Select All not found and No Items message absent??")
                    sys.exit(1)

            print("Clicking Select All...")
            page.check("input[name='select-all']")
            
            # 2. Check for Bulk Bar
            print("Waiting for Bulk Action Bar...")
            bar = page.wait_for_selector("text=items selected", timeout=2000)
            if not bar:
                print("FAILURE: Bulk bar not appeared.")
                sys.exit(1)
                
            text = bar.inner_text()
            print(f"Bar Text: {text}")
            
            # 3. Click Clear
            print("Clicking Clear...")
            page.click("text=Clear")
            
            time.sleep(0.5)
            if page.is_visible("text=items selected"):
                 print("FAILURE: Bulk bar did not disappear.")
                 sys.exit(1)

            print("SUCCESS: Bulk Actions verified.")

        except Exception as e:
            print(f"ERROR: {e}")
            page.screenshot(path="bulk_failure.png")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    verify_bulk_actions()
