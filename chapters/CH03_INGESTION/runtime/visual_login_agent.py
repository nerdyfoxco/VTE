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
        self.profile_path = os.path.join(os.path.dirname(self.cookie_path), "..", "auth_profiles", "appfolio.json")
        self.learned_path = [] # For recording Tier 3 actions

    def validate_session(self) -> bool:
        """Tier 1: Checks if existing cookies provide access to Dashboard."""
        if not os.path.exists(self.cookie_path):
            logger.info("[Tier 1] No cookies found.")
            return False
            
        logger.info("[Tier 1] Validating Session Cookies...")
        self.start_browser()
        
        # Load Cookies
        with open(self.cookie_path, 'r') as f:
            cookies = json.load(f)
            self.browser_context.add_cookies(cookies)
            
        try:
            self.page.goto("https://anchorrealty.appfolio.com/dashboard", timeout=15000)
            self.page.wait_for_load_state("networkidle")
            
            # Check for specific dashboard elements or URL
            if "dashboard" in self.page.url and "Sign In" not in self.page.title():
                logger.info("[Tier 1] Success: Session is Valid.")
                return True
            else:
                logger.warning("[Tier 1] Failed: Redirected to Login.")
                return False
        except Exception as e:
            logger.error(f"[Tier 1] Validation Error: {e}")
            return False
    def start_browser(self):
        if self.page and not self.page.is_closed():
            logger.info("[Browser] Reusing existing session.")
            return

        logger.info("[Browser] Launching Playwright...")
        try:
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
            logger.info("[Browser] Launched.")
        except Exception as e:
            logger.error(f"[Browser] Launch Failed: {e}")
            raise

    def _get_screenshot_base64(self) -> str:
        """Captures screenshot and returns base64 string for LLM."""
        try:
            screenshot_bytes = self.page.screenshot(type="jpeg")
            return base64.b64encode(screenshot_bytes).decode('utf-8')
        except Exception as e:
            logger.error(f"[Vsion] Screenshot Failed: {e}")
            return ""

    def login_using_profile(self) -> bool:
        """Tier 2: Replays a learned selector path."""
        if not os.path.exists(self.profile_path):
            return False
            
        logger.info("[Tier 2] Profiler Found. Attempting Replay...")
        try:
            with open(self.profile_path, 'r') as f:
                path_steps = json.load(f)
                
            self.start_browser()
            self.page.goto("https://anchorrealty.appfolio.com/users/sign_in")
            
            for step in path_steps:
                action = step.get("action")
                selector = step.get("selector")
                desc = step.get("desc", selector)
                
                logger.info(f"[Tier 2] Replaying: {action} on {desc}")
                
                if action == "FILL":
                    value_key = step.get("value")
                    val = os.getenv(value_key) if value_key in ["EMAIL_USER", "EMAIL_PASS"] else value_key
                    self.page.fill(selector, val)
                elif action == "CLICK":
                    self.page.click(selector, timeout=5000)
                elif action == "PRESS":
                    self.page.press(selector, step.get("key"))
                    
                self.page.wait_for_timeout(1000) # Human-like pace
                
            self.page.wait_for_load_state("networkidle")
            
            # Validation
            if "dashboard" in self.page.url:
                logger.info("[Tier 2] Success: Replay Login Complete.")
                # Save Cookies
                cookies = self.browser_context.cookies()
                with open(self.cookie_path, 'w') as f:
                    json.dump(cookies, f)
                return True
            else:
                logger.warning("[Tier 2] Replay Failed (URL mismatch). Falling back to Vision.")
                return False
                
        except Exception as e:
            logger.error(f"[Tier 2] Replay Failed: {e}")
            return False

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
                 # Try to click by text
                 try:
                     self.page.click(f"text={target_text}", timeout=2000)
                     # Record for Tier 2
                     self.learned_path.append({"action": "CLICK", "selector": f"text={target_text}", "desc": target_text})
                 except:
                     # Fallback for "Send Verification Code"
                     if "Send" in target_text:
                         logger.info("Trying fallback selectors for Send button...")
                         self.page.click('input[type="submit"]', timeout=2000)
                         self.learned_path.append({"action": "CLICK", "selector": 'input[type="submit"]', "desc": "Send Button"})
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
            
            # Record for Tier 2
            self.learned_path.append({"action": "FILL", "selector": 'input[name="user[email]"]', "value": "EMAIL_USER"})
            self.learned_path.append({"action": "FILL", "selector": 'input[name="user[password]"]', "value": "EMAIL_PASS"})
            self.learned_path.append({"action": "PRESS", "selector": 'input[name="user[password]"]', "key": "Enter"})
            
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
                logger.info("OTP Submitted (Enter Key). Waiting for transition...")
                
                # Wait longer for redirect (sometimes slow)
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15000)
                except:
                    logger.warning("NetworkIdle timeout (15s), proceeding to check state anyway...")

                return self.analyze_state_and_act(email, password, last_action="Entered OTP")
            except Exception as e:
                logger.error(f"Failed to enter OTP: {e}")
                return False

        elif action == "FINISH":
            logger.info("[Act] Login Complete. Dashboard Detected.")
            # Save Learned Path (Tier 2 Enablement)
            if self.learned_path:
                try:
                    os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
                    with open(self.profile_path, 'w') as f:
                        json.dump(self.learned_path, f, indent=2)
                    logger.info(f"[Tier 3] Learned Path Saved ({len(self.learned_path)} steps).")
                except Exception as e:
                    logger.error(f"Failed to save auth profile: {e}")
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
        # Tier 1: Session Resume
        if self.validate_session():
            logger.info("Login Success via Tier 1 (Cookies).")
            return

        # Tier 2: Learned Path Replay
        if self.login_using_profile():
            logger.info("Login Success via Tier 2 (Replay).")
            self.browser.close()
            return

        # Tier 3: Visual Intelligence (Fallback)
        logger.info("[Tier 3] Fallback to Visual Intelligence...")
        
        # Ensure browser is running (idempotent)
        self.start_browser()
        
        # Only navigate if we aren't already there (e.g. from Tier 2 failure)
        if self.page.url == "about:blank":
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
