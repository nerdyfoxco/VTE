import os
import json
from datetime import datetime
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright, Page, TimeoutError

class AppFolioLiveAdapter:
    """
    VTE 'Eyes' Integration for AppFolio.
    Authenticates, navigates to delinquency ledgers, scrapes unstructured data,
    and returns it formatted for the strict VTE Policy Engine envelope.
    """
    def __init__(self, tenant_id: str, email: str, password: str, base_url: str):
        self.tenant_id = tenant_id
        self.email = email
        self.password = password
        self.base_url = base_url

    def _login(self, page: Page):
        """Securely authenticates the Playwright session."""
        print(f"[Eyes] Authenticating AppFolio session for {self.email}...")
        page.goto(f"{self.base_url}/users/sign_in")
        
        # Wait for the email field
        page.fill("input[name='user[email]']", self.email)
        page.fill("input[name='user[password]']", self.password)
        page.click("input[type='submit']")
        
        # Wait for Dashboard to confirm successful login
        try:
             page.wait_for_selector(".dashboard-welcome, .top-nav", timeout=15000)
             print("[Eyes] Authentication Successful.")
        except TimeoutError:
             raise Exception("[Eyes - Critical] AppFolio Authentication failed or was challenged by MFA.")

    def _scrape_tenant_ledger(self, page: Page, tenant_url_suffix: str) -> Dict[str, Any]:
        """
        Navigates to a specific tenant ledger, extracting unstructured text.
        In a real implementation, selectors are highly specific to AppFolio's DOM.
        """
        target_url = f"{self.base_url}/{tenant_url_suffix}"
        print(f"[Eyes] Navigating to target ledger: {target_url}")
        page.goto(target_url)
        
        # 1. Scrape Balance
        try:
             # Wait for the balance pill
             balance_element = page.wait_for_selector(".js-total-balance, .tenant-balance", timeout=10000)
             raw_balance = balance_element.inner_text() if balance_element else "$0.00"
             # Clean string: "$1,250.50" -> 1250.50
             clean_balance = float(raw_balance.replace("$", "").replace(",", "").strip())
        except TimeoutError:
             clean_balance = 0.0
             
        # 2. Scrape Name & Status
        tenant_name = page.locator(".tenant-name-header h1").inner_text() if page.locator(".tenant-name-header h1").count() > 0 else "Unknown Resident"
        status_tag = page.locator(".tenant-status-label").inner_text().lower() if page.locator(".tenant-status-label").count() > 0 else "unknown"

        # 3. Scrape Tags (For DNC / VIP / Eviction analysis)
        raw_tags = []
        tags_locators = page.locator(".tenant-tags .tag")
        for i in range(tags_locators.count()):
             raw_tags.append(tags_locators.nth(i).inner_text().lower())
             
        # 4. Scrape Unstructured Notes (For Sickness/Death analysis)
        raw_notes = ""
        notes_locators = page.locator(".tenant-notes-section p, .notes-block")
        for i in range(notes_locators.count()):
             raw_notes += notes_locators.nth(i).inner_text() + " "

        return {
            "balance_owed": clean_balance,
            "status": "delinquent" if clean_balance > 0 else "current",
            "tenant_name": tenant_name,
             # Pass the raw scraped text directly to the Brain for keyword scanning
            # The Brain will determine `dnc_active` and `death_sickness` from these
            "raw_tags_scraped": raw_tags, 
            "raw_notes_scraped": raw_notes,
            # Synthesize water bill data based on recent ledger line items 
            # (Mocked here for the adapter logic)
            "is_only_new_water": "water" in raw_notes.lower() and clean_balance < 100,
            "has_legal_action": "eviction" in raw_notes.lower() or "jba" in raw_tags
        }

    def fetch_and_map_ledger(self, tenant_url_suffix: str) -> Dict[str, Any]:
        """Orchestrates the synchronous Playwright scrape and maps to the VTE Envelope."""
        with sync_playwright() as p:
            # Headless true for production operations
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="VTE Operating System/1.0 (Integration/AppFolio)"
            )
            page = context.new_page()
            
            try:
                self._login(page)
                scraped_data = self._scrape_tenant_ledger(page, tenant_url_suffix)
            except Exception as e:
                browser.close()
                raise e
                
            browser.close()
            
            # Pack extracted data into the standardized Engine ingestion format
            # This is the exact shape `appfolio.py` expects from the mock tester
            return {
                "balance_owed": scraped_data["balance_owed"],
                "is_only_new_water": scraped_data["is_only_new_water"],
                "has_legal": scraped_data["has_legal_action"],
                
                # We map the raw strings into boolean flags for the strict JSON schema
                "dnc_active": any("do not contact" in tag.lower() or "dnc" in tag.lower() for tag in scraped_data["raw_tags_scraped"]),
                "death_sickness": "passed away" in scraped_data["raw_notes_scraped"].lower() or "hospital" in scraped_data["raw_notes_scraped"].lower(),
                
                "status": scraped_data["status"],
                "tenant_name": scraped_data["tenant_name"]
            }

if __name__ == "__main__":
    # Test execution harness
    scraper = AppFolioLiveAdapter(
        tenant_id="ws_real", 
        email="test_operator@vte.com", 
        password="mock_password", 
        base_url="https://mock-appfolio-domain.com"
    )
    print("Scraper Module Initialized. Ready for CRON trigger.")
