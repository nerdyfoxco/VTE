import pytest
import uuid
import re
from playwright.sync_api import Page, expect

# Requires the React Dev Server running on 5173 and FastAPI on 8080
FRONTEND_URL = "http://localhost:5173"

def test_frontend_signup_flow(page: Page):
    """
    Simulates a new Operator provisioning an Identity.
    Verifies the React app intercepts the 201 CREATED and renders the TOTP URI.
    """
    unique_email = f"operator_{uuid.uuid4()}@vte.com"
    
    # 1. Navigate to Login
    page.goto(f"{FRONTEND_URL}/login")
    expect(page.locator("h2")).to_contain_text("VTE Identity")
    
    # 2. Proceed to Provisioning
    page.click("text=Request Access")
    expect(page.url).to_contain("/signup")
    
    # 3. Fill Out Strict Invariants
    page.fill("input[placeholder=\"Kevin O'Leary\"]", "E2E Test Operator")
    page.fill("input[placeholder=\"operator@vte.com\"]", unique_email)
    page.fill("input[placeholder=\"tnt_vte_1\"]", "tnt_vte_1")
    page.fill("input[placeholder=\"••••••••••••\"]", "StrongPassword123!")
    
    # 4. Submit
    page.click("button:has-text('Provision Identity')")
    
    # 5. Verify the abstract 'Identity Created' component mounts
    expect(page.locator("h2")).to_contain_text("Identity Created")
    
    # 6. Verify the TOTP URI is physically present
    totp_element = page.locator("code")
    expect(totp_element).to_be_visible()
    totp_text = totp_element.inner_text()
    assert "otpauth://totp" in totp_text
    assert unique_email in totp_text

def test_frontend_signin_mfa_interception(page: Page):
    """
    Simulates a login attempt.
    Verifies the React app correctly routes the MFA_REQUIRED challenge to /mfa.
    """
    unique_email = f"operator_{uuid.uuid4()}@vte.com"
    
    # Fast-path Provisioning (Bypass UI for speed)
    page.request.post("http://127.0.0.1:8080/auth/signup", data={
        "email": unique_email,
        "password": "StrongPassword123!",
        "full_name": "E2E Signin Test",
        "tenant_id": "tnt_vte_1"
    })
    
    # 1. Execute Login Flow
    page.goto(f"{FRONTEND_URL}/login")
    page.fill("input[type=\"email\"]", unique_email)
    page.fill("input[type=\"password\"]", "StrongPassword123!")
    page.click("button:has-text('Authenticate')")
    
    # 2. Verify we hit the router intercept for MFA
    expect(page).to_have_url(re.compile(r".*/mfa$"))
    
    # 3. Verify the Challenge UI
    expect(page.locator("h2")).to_contain_text("MFA Required")
    expect(page.locator("p")).to_contain_text(unique_email)
    
    # 4. Test Invalid Verification
    page.fill("input[placeholder=\"000000\"]", "123456")
    page.click("button:has-text('Verify Identity')")
    expect(page.locator("text=Invalid or expired")).to_be_visible()

def test_protected_dashboard_kicks_to_login(page: Page):
    """
    Guarantees the `ProtectedRoute` wrapper functions.
    Navigating directly to root without a session token must Fail-Closed.
    """
    page.goto(FRONTEND_URL)
    expect(page).to_have_url(re.compile(r".*/login$"))
