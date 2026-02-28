from playwright.sync_api import sync_playwright

def verify_appfolio():
    print("Beginning validation of Native AppFolio Integration Flow...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            print("1. Loading Integrations Page...")
            page.goto("http://localhost:3001/integrations/appfolio")
            page.wait_for_timeout(2000)
            
            print("2. Verifying Native React Mount...")
            button = page.locator('button:has-text("Boot AppFolio Scraper")')
            if button.count() > 0:
                print("SUCCESS: React AppFolio Button Mounted.")
                
                print("3. Triggering Boot Execution...")
                button.click()
                page.wait_for_timeout(2000)
                
                status = page.locator('.text-xl.font-medium.text-emerald-400')
                if status.count() > 0:
                   print(f"SUCCESS: System State is now: {status.inner_text()}")
                
            else:
                print("FAILED: Boot Button not found.")
                
            page.screenshot(path="appfolio_integration_test.png", full_page=True)
            print("Test Complete. Screenshot saved.")
            
        except Exception as e:
            print(f"E2E Integration Test Failed: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    verify_appfolio()
