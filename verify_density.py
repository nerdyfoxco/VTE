import time
from playwright.sync_api import sync_playwright
import sys

def verify_density():
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
            
            # Wait for items to load
            page.wait_for_selector("text=Showing", timeout=10000)
            
            # Check for Toggle Button
            print("Locating Density Toggle...")
            toggle_btn = page.locator("#btn-toggle-density")
            if not toggle_btn.is_visible():
                print("FAILURE: Density toggle button not found.")
                sys.exit(1)
                
            # Initial State: Comfortable
            # Check padding of first row item (should be py-4 = 16px)
            # We can't easily check 'py-4' class if it's compiled, but we can check the text or attribute if we added one.
            # Or we check the svg icon usage.
            
            print("Clicking Toggle -> Compact...")
            toggle_btn.click()
            time.sleep(1) # Wait for render
            
            # Check for Compact Icon/Text
            if "Compact" not in toggle_btn.inner_text():
                 print("FAILURE: Text did not change to Compact.")
                 
            # Verify localStorage
            val = page.evaluate("localStorage.getItem('vte_density')")
            if val != "compact":
                print(f"FAILURE: localStorage value is {val}, expected 'compact'")
                sys.exit(1)
                
            print("Clicking Toggle -> Comfortable...")
            toggle_btn.click()
            time.sleep(1)
            
            val = page.evaluate("localStorage.getItem('vte_density')")
            if val != "comfortable":
                 print(f"FAILURE: localStorage value is {val}, expected 'comfortable'")
                 sys.exit(1)

            print("SUCCESS: Density Toggle verified.")

        except Exception as e:
            print(f"ERROR: {e}")
            page.screenshot(path="density_failure.png")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    verify_density()
