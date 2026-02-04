import os
import time
import base64
import json
from playwright.sync_api import sync_playwright, Page, BrowserContext
from foundation.runtime.config import config
from foundation.runtime.vte_logger import configure_logger
from chapters.CH14_INTELLIGENCE.runtime.brain_client import BrainClient

logger = configure_logger("VISUAL_AGENT")

class VisualLoginAgent:
    def __init__(self, headless=False):
        self.headless = headless
        self.browser_context: BrowserContext = None
        self.page: Page = None
        self.brain = BrainClient()
        self.cookie_path = config.appfolio_cookie_path

    def start_browser(self):
        self.playwright = sync_playwright().start()
        # Launch options for maximum visibility/stability
        launch_args = ["--start-maximized", "--disable-blink-features=AutomationControlled"]
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=1000, # Slow down to avoid "m" typing errors and let user see
            args=launch_args
        )
        self.browser_context = self.browser.new_context(no_viewport=True)
        self.page = self.browser_context.new_page()

    def _get_screenshot_base64(self) -> str:
        """Captures screenshot and returns base64 string for LLM."""
        try:
            screenshot_bytes = self.page.screenshot(type="jpeg")
            return base64.b64encode(screenshot_bytes).decode('utf-8')
        except Exception as e:
            logger.error(f"[Vsion] Screenshot Failed: {e}")
            return ""

    def analyze_state_and_act(self, email, password, last_action=None):
        """
        The Core Loop: See -> Think -> Act.
        Returns True if Logged In.
        """
        logger.info("[Vision] Analyzing Screen...")
        b64_img = self._get_screenshot_base64()
        
        # Determine Page State via Brain
        prompt = f"""
        You are an AI Agent logging into AppFolio. 
        Current Credentials available: Email='{email}', Password='[HIDDEN]'.
        Last Action Taken: {last_action}
        
        Analyze the screenshot. 
        1. Identify the current state (Login Page, Dashboard, OTP Challenge, MFA Selection, Error).
        2. Decide the next action.
        3. If Last Action was clicking an option (e.g. SMS), look for a Submit/Send button.
        
        Respond ONLY in JSON format:
        {{
            "state": "LOGIN_FORM" | "DASHBOARD" | "OTP_REQUIRED" | "MFA_SELECTION" | "ERROR",
            "action": "TYPE_CREDS" | "ENTER_OTP" | "CLICK" | "FINISH" | "ABORT",
            "target_text": "text on button to click (if action is CLICK)",
            "reason": "explanation"
        }}
        """
        
        # ... (Rest of code) ...
        
        # Recurse with last_action
        
        # We need a multimodal call here.
        # Since BrainClient wrapper might only support text, we will assume 
        # for this specific Agent we construct the payload manually for OpenAI if needed,
        # OR we rely on DOM text as a fallback if Vision isn't enabled in the standard client.
        # ALLOWING DOM TEXT FOR NOW AS ROBUST FALLBACK + FAST EXECUTION
        
        try:
            self.page.wait_for_selector("body", timeout=10000)
            body_text = self.page.eval_on_selector("body", "el => el.innerText")
            input_values = self.page.evaluate('''() => {
                return Array.from(document.querySelectorAll('input[type="submit"], input[type="button"], button')).map(e => e.value || e.innerText).join('\\n');
            }''')
            page_text = body_text + "\n[BUTTONS/INPUTS]:\n" + input_values
            
            with open("page_dump.txt", "w", encoding="utf-8") as f:
                f.write(page_text)
        except:
            page_text = "ERROR: Body not found or empty."
            
        logger.info(f"[Vision] Visible Text: {page_text[:500]}")
        prompt_text = f"{prompt}\n\nExisting Text on Page:\n{page_text[:2000]}"
        
        response_text = self.brain.think(prompt_text)
        
        # Parse JSON from Brain (handling potential markdown fences)
        try:
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            decision = json.loads(clean_json)
            logger.info(f"[Brain] Decision: {decision}")
        except Exception as e:
            logger.error(f"[Brain] Failed to parse JSON: {response_text}")
            return False

        action = decision.get("action")
        target_text = decision.get("target_text", "")

        if action == "CLICK":
             logger.info(f"[Act] Clicking Element with text: '{target_text}'")
             try:
                 # Try to click by text
                 try:
                     self.page.click(f"text={target_text}", timeout=2000)
                 except:
                     # Fallback for "Send Verification Code"
                     if "Send" in target_text:
                         logger.info("Trying fallback selectors for Send button...")
                         self.page.click('input[type="submit"]', timeout=2000)
                     else:
                         raise

                 self.page.wait_for_timeout(3000) # Wait for animation/selection
                 self.page.wait_for_load_state("networkidle")
                 return self.analyze_state_and_act(email, password, last_action=f"Clicked '{target_text}'")
             except Exception as e:
                 logger.error(f"Failed to Click '{target_text}': {e}")
                 return False

        if action == "TYPE_CREDS":
            logger.info("[Act] Typing Credentials...")
            # Robust typing
            self.page.fill('input[name="user[email]"]', "") # Clear first
            self.page.type('input[name="user[email]"]', email, delay=100)
            
            self.page.fill('input[name="user[password]"]', "")
            self.page.type('input[name="user[password]"]', password, delay=100)
            
            logger.info("[Act] Submitting...")
            self.page.press('input[name="user[password]"]', 'Enter')
            self.page.wait_for_load_state("networkidle")
            return self.analyze_state_and_act(email, password, last_action="Typed Credentials") # Recurse/Check next state

        elif action == "ENTER_OTP":
            logger.warning(">>> HITL REQUIRED: OTP DETECTED <<<")
            otp_code = input("\n[USER INPUT REQUIRED] Enter the AppFolio OTP Code: ")
            
            # Brain likely didn't tell us the selector, so we guess standard ones or ask Brain again.
            # For robustness, we'll try common OTP fields.
            try:
                # Try generic input that looks like OTP
                if self.page.is_visible('input[name="user[otp_code]"]'):
                     self.page.type('input[name="user[otp_code]"]', otp_code)
                elif self.page.is_visible('input[type="text"]'):
                     # Fallback to first text input if it's the only one
                     self.page.type('input[type="text"]', otp_code)
                
                self.page.press('body', 'Enter')
                logger.info("OTP Submitted. Waiting for transition...")
                self.page.wait_for_timeout(5000) # Wait for redirect
                self.page.wait_for_load_state("networkidle")
                return self.analyze_state_and_act(email, password, last_action="Entered OTP")
            except Exception as e:
                logger.error(f"Failed to enter OTP: {e}")
                return False

        elif action == "FINISH":
            logger.info("[Act] Login Complete. Dashboard Detected.")
            return True

        elif action == "ABORT":
            failure_reason = decision.get('reason')
            logger.error(f"[Act] Aborting: {failure_reason}")
            try:
                self.page.screenshot(path="latest_failure.jpg", type="jpeg")
                logger.info("Saved failure screenshot to 'latest_failure.jpg'")
            except:
                pass
            return False
            
        return False

    def login(self, email, password):
        self.start_browser()
        url = "https://anchorrealty.appfolio.com/users/sign_in"
        logger.info(f"Navigating to AppFolio: {url}")
        self.page.goto(url)
        
        success = self.analyze_state_and_act(email, password)
        
        if success:
            cookies = self.browser_context.cookies()
            os.makedirs(os.path.dirname(self.cookie_path), exist_ok=True)
            with open(self.cookie_path, 'w') as f:
                json.dump(cookies, f)
            logger.info("Session Saved.")
            
        # Hold for inspection
        time.sleep(5)
        self.browser.close()

if __name__ == "__main__":
    # Test Run
    agent = VisualLoginAgent(headless=False)
    agent = VisualLoginAgent(headless=False)
    email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    if not email or not password:
        logger.error("EMAIL_USER and EMAIL_PASS must be set in Environment.")
        exit(1)

    agent.login(email, password)
