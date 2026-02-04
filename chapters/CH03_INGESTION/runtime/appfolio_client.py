import os
import json
import logging
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from foundation.runtime.config import config
from foundation.runtime.vte_logger import configure_logger

logger = configure_logger("APPFOLIO_CLIENT")

class AppFolioClient:
    """
    Playwright-based client for AppFolio.
    Handles Cookie persistence and Page Navigation.
    """
    def __init__(self, headless: bool = True, slow_mo: int = 0):
        self.headless = headless
        self.slow_mo = slow_mo
        # If user explicitly requests visible browser, we allow it.
        if os.getenv("VTE_HEADLESS", "true").lower() == "false":
            self.headless = False
            
        self.cookie_path = config.appfolio_cookie_path
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        
        logger.info(f"Initializing AppFolio Client (Headless={headless})")

    def _load_cookies(self):
        """Loads cookies from storage if they exist."""
        if os.path.exists(self.cookie_path):
            try:
                with open(self.cookie_path, 'r') as f:
                    cookies = json.load(f)
                    self.context.add_cookies(cookies)
                logger.info("Session Config Rehydrated (Cookies Loaded)")
                return True
            except Exception as e:
                logger.error(f"Failed to load cookies: {e}")
                return False
        else:
            logger.warning("No Cookie File Found (Needs HITL Auth)")
            return False

    def start(self):
        """Starts the Browser and Context."""
        self.p = sync_playwright().start()
        launch_args = ["--start-maximized"] if not self.headless else []
        self.browser = self.p.chromium.launch(
            headless=self.headless, 
            slow_mo=self.slow_mo,
            args=launch_args
        )
        self.context = self.browser.new_context(no_viewport=True) # Full size
        
        if self._load_cookies():
            logger.info("Ready: Authenticated Session")
        else:
            logger.info("Ready: Guest Session (Login Required)")
            
        self.page = self.context.new_page()

    def login_interactive(self):
        """
        Pauses execution to allow user to log in manually.
        Waits for user to press ENTER in console.
        """
        if self.headless:
            logger.warning("Cannot perform interactive login in Headless mode.")
            return

        logger.info(">>> INTERACTIVE LOGIN REQUIRED <<<")
        logger.info("Please log in to AppFolio in the browser window.")
        logger.info("Once logged in, press ENTER in this terminal to save cookies.")
        input("Press ENTER to continue...")
        
        # Save Cookies
        cookies = self.context.cookies()
        os.makedirs(os.path.dirname(self.cookie_path), exist_ok=True)
        with open(self.cookie_path, 'w') as f:
            json.dump(cookies, f)
        logger.info("Cookies Saved. Session Persisted.")

    def login_auto(self, email, password):
        """
        Attempts to auto-fill the login form.
        """
        if self.headless:
            logger.warning("Auto-login should be watched (Headless=False).")
        
        logger.info(f"Attempting Auto-Login for {email}")
        try:
            # Common AppFolio Selectors (Best Guess - will need adjustment if changed)
            print("[Agent] Typing Email: " + email)
            self.page.type('input[name="user[email]"]', email, delay=100)
            
            print("[Agent] Typing Password: ********")
            self.page.type('input[name="user[password]"]', password, delay=100)
            
            print("[Agent] Pressing ENTER to Login...")
            self.page.press('input[name="user[password]"]', 'Enter')
            
            self.page.wait_for_load_state("networkidle")
            
            # Save Cookies
            cookies = self.context.cookies()
            os.makedirs(os.path.dirname(self.cookie_path), exist_ok=True)
            with open(self.cookie_path, 'w') as f:
                json.dump(cookies, f)
            logger.info("Auto-Login Complete. Cookies Saved.")
        except Exception as e:
            logger.error(f"Auto-Login Failed (Selectors might be wrong): {e}")

    def close(self):
        """Clean shutdown."""
        if self.browser:
            self.browser.close()
        if self.p:
            self.p.stop()
        logger.info("Browser Shutdown")

    def navigate_to_tenant(self, tenant_id: str) -> bool:
        """
        Navigates to a specific tenant page.
        URL pattern: https://anchorrealty.appfolio.com/users/12345/tenants/{tenant_id}
        """
        if not self.page:
            logger.error("Browser not started.")
            return False
            
        try:
            # We assume a standard URL structure. 
            # In reality, this might need dynamic discovery or use the 'Global Search' box.
            # Using specific URL for now as placeholder.
            target_url = f"https://anchorrealty.appfolio.com/tenants/{tenant_id}"
            logger.info(f"Navigating to Tenant: {tenant_id} ({target_url})")
            
            self.page.goto(target_url)
            self.page.wait_for_load_state("networkidle")
            
            # Verify we are on the right page
            if "Page Not Found" in self.page.title():
                 logger.error("Tenant Page Not Found")
                 return False
                 
            return True
        except Exception as e:
            logger.error(f"Navigation Failed: {e}")
            return False

    def write_note(self, content: str, dry_run: bool = False) -> bool:
        """
        Writes a note to the current Tenant page.
        """
        if not self.page:
             return False

        logger.info(f"Writing Note: '{content}' (DryRun={dry_run})")
        
        try:
            # 1. Click 'Notes' tab or finding the Note input
            # Selectors based on AppFolio UI experience (Hypothetical)
            self.page.click("text=Notes", timeout=2000) 
            
            # 2. Type Content
            self.page.fill('textarea[placeholder="Add a note..."]', content)
            
            # 3. Save
            if not dry_run:
                self.page.click('button:has-text("Save")')
                self.page.wait_for_load_state("networkidle")
                logger.info("Note Saved.")
            else:
                logger.info("[DRY RUN] Would have clicked Save.")
                
            return True
        except Exception as e:
            logger.error(f"Write Note Failed: {e}")
            return False

if __name__ == "__main__":
    # Canary
    try:
        client = AppFolioClient(headless=True)
        client.start()
        print("AppFolio Client Initialized")
        client.close()
    except Exception as e:
        print(f"FATAL: {e}")
