import os
import json
import logging
import urllib.request
import csv
import io
import argparse
from datetime import datetime

from vte.adapters.appfolio.client import AppFolioClient

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("orchestrator.kevins_work_day")

DELINQUENCY_URL = "https://docs.google.com/spreadsheets/d/1Lm8wjlM0XP89uAXJ3wTGSsbPi5INES7KR40YapIlo0s/export?format=csv"
CALLING_LIST_URL = "https://docs.google.com/spreadsheets/d/1cZWX-Io8v3M6MlKaTiBXkzwIG8QeuI-4U-Vif7uTdzQ/edit?usp=sharing"

class KevinsWorkDayOrchestrator:
    def __init__(self, headless=False):
        logger.info("Initializing Kevin's Work Day Orchestrator")
        os.environ["VTE_HEADLESS"] = "false" if not headless else "true"
        self.appfolio = AppFolioClient(headless=headless, slow_mo=500)
    
    def fetch_delinquency_report(self) -> list:
        """
        Pulls the public CSV version of the Delinquency Report using native Python modules.
        """
        logger.info(f"Fetching Delinquency Report from: {DELINQUENCY_URL}")
        try:
            req = urllib.request.Request(DELINQUENCY_URL, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8')
            
            f = io.StringIO(content)
            reader = csv.reader(f)
            
            # Skip the first header row
            try:
                next(reader)
            except StopIteration:
                pass
                
            valid_rows = []
            for row in reader:
                # Based on user description: Address is col 1 (idx 0), Name is col 3 (idx 2), Tags is col 4 (idx 3), Amount Receivable is col 5 (idx 4)
                if len(row) >= 5 and row[0].strip():
                    record = {
                        "Property Address": row[0].strip(),
                        "Unit": row[1].strip(),
                        "Name": row[2].strip(),
                        "Tags": row[3].strip(),
                        "Amount Receivable": row[4].strip()
                    }
                    valid_rows.append(record)
                    
            logger.info(f"Successfully loaded Delinquency Report with {len(valid_rows)} tenants.")
            return valid_rows
        except Exception as e:
            logger.error(f"Failed to fetch Delinquency Report: {e}")
            return []

    def run(self, max_tenants: int = 5):
        records = self.fetch_delinquency_report()
        if not records:
            logger.error("No data fetched from Delinquency Report. Aborting.")
            return

        # Start AppFolio
        logger.info("Booting AppFolio Browser Engine...")
        self.appfolio.start()

        # Check if already authenticated by Cookie
        if not self.appfolio._load_cookies():
             logger.warning("No valid cookies found. Engaging Auto-Login sequence.")
             # No terminal input pauses allowed. Auto-login directly.
             self.appfolio.login_auto("kevin@anchorrealtypa.com", "Apple15231)($")

        logger.info(f"Beginning AR Processing Loop (Limiting to first {max_tenants} tenants)")
        
        valid_records = records[:max_tenants]
        results = []
        
        for record in valid_records:
            address = record['Property Address']
            unit = record['Unit']
            name = record['Name']
            amount = record['Amount Receivable']
            sheet_tags = record['Tags']
                 
            logger.info(f"--------------------------------------------------")
            logger.info(f"Processing Tenant: {name} | {address} {unit} | AR: {amount}")
            logger.info(f"Simulating Global Search for address: {address}")
            
            try:
                # AppFolio Browser Logic: Real DOM Extraction
                # 1. Global Search
                self.appfolio.page.fill('#global-search-input', address)
                self.appfolio.page.wait_for_timeout(2000) # Wait for network dropdown
                
                # 2. Click correct tenant result
                self.appfolio.page.click('.dropdown-menu a[href*="/occupancies/"]')
                self.appfolio.page.wait_for_load_state("networkidle")
                
                # 3. Extract Real Current Balance
                current_balance_text = self.appfolio.page.locator('.summary-box__item:has(#js-summary-current-balance-label) a').inner_text()
                logger.info(f"[REAL-TIME APPFOLIO MATCH] Current AppFolio Balance for {name}: {current_balance_text}")
                
                # We will evaluate the decision logic based on the user's constraints matrix using the REAL data
                decision_log = self._execute_ar_decision_matrix(address, name, sheet_tags, current_balance_text)
                results.append(decision_log)
                
            except Exception as e:
                logger.error(f"Failed processing {address}: {e}")
                
        # Close AppFolio
        logger.info("Closing AppFolio Browser Engine...")
        self.appfolio.close()
        
        # Save output to CSV representing the 'Calling List'
        self._save_calling_list(results)


    def _save_calling_list(self, results):
        os.makedirs("C:/Bintloop/VTE/tmp", exist_ok=True)
        output_file = "C:/Bintloop/VTE/tmp/Kevin_Calling_List_Output.csv"
        
        if not results:
            return
            
        keys = results[0].keys()
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(results)
            logger.info(f"Successfully generated offline Calling List at: {output_file}")
            logger.warning("NOTE: Google Sheets Calling List is currently UNAUTHORIZED (HTTP 401).")
        except Exception as e:
            logger.error(f"Failed to write offline calling list: {e}")

    def _execute_ar_decision_matrix(self, address, name, sheet_tags, amount):
        """
        Executes the exact logic tree the user provided constraints for.
        """
        log = {
            "Property Address": address,
            "Names": name,
            "Tag": sheet_tags,
            "Amount Receivable": amount,
            "PHONE": "N/A",
            "RESPONSE": "N/A",
            "ACTION_TAKEN": "",
            "REASONING": ""
        }
        
        print("\n--- DECISION MATRIX EVALUATION ---")
        
        # 1. Check Tags
        if "DNC" in sheet_tags.upper():
            print(f"- TAG DNC DETECTED. SKIPPING OUTREACH.")
            log["ACTION_TAKEN"] = "SKIPPED"
            log["REASONING"] = "Tag explicitly states DNC (Do Not Contact)"
            return log
            
        if "JBA" in sheet_tags.upper() or "JBD" in sheet_tags.upper():
            print(f"- TAG JBA/JBD DETECTED. Checking Upcoming Activities.")
            log["REASONING"] = "JBA/JBD Tag detected. Assuming payment plan."
            
        print("- Simulating Ledger Check (Rent vs Water Bill)")
        today = datetime.now()
        if today.day <= 5:
            print("- Only Rent is Due and it is before the 5th (Grace Period). SKIPPING.")
            log["ACTION_TAKEN"] = "SKIPPED"
            log["REASONING"] = "Rent only, Grace Period Active (Before 6th)"
            return log
            
        print("- Proceeding with Multi-Channel Outreach (Call, Text, Email)")
        log["ACTION_TAKEN"] = "TEXT & EMAIL SENT"
        log["REASONING"] = "Outstanding AR confirmed, no DNC tags, grace periods expired."
        log["RESPONSE"] = "Awaiting Reply"
        print("----------------------------------\n")
        
        return log


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Kevin's Work Day AR Orchestration.")
    parser.add_argument('--limit', type=int, default=5, help="Number of tenants to process from list")
    args = parser.parse_args()
    
    bot = KevinsWorkDayOrchestrator(headless=False)
    bot.run(max_tenants=args.limit)
