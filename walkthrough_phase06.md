# Phase 06: Intelligent Visual Agent (Walkthrough)

**Success**: The `VisualLoginAgent` successfully navigated a complex, multi-step MFA login flow entirely driven by AI (Brain).

## 1. Capabilities Demonstrated
- **"See -> Think -> Act" Loop**: The Agent captured screenshots, analyzed them via OpenAI (GPT-4), and decided the next action autonomously.
- **Dynamic Navigation**:
    1.  **Login Page**: Identified specific credentials needed.
    2.  **MFA Selection**: Recognized the need to choose a verification method. **Brain Decision**: "Click 'Receive code via SMS'".
    3.  **Send Code**: Recognized the "Send Verification Code" button (via fallback logic) and clicked it.
    4.  **OTP Entry**: Detected the "Enter Code" screen and paused for **HITL (Human-In-The-Loop)** input.
- **Self-Healing**:
    -   Recovered from "Invisible Button" issues by extracting DOM values.
    -   Fixed "Click Loops" by implementing Short-Term Memory (`last_action`).

## 2. Verification Evidence
### Execution Log
```text
[INFO] VISUAL_AGENT: [Brain] Decision: {'state': 'MFA_SELECTION', 'action': 'CLICK', 'target_text': 'Receive code via SMS'}
[INFO] VISUAL_AGENT: [Act] Clicking Element with text: 'Receive code via SMS'
...
[INFO] VISUAL_AGENT: [Brain] Decision: {'state': 'OTP_REQUIRED', 'action': 'ENTER_OTP'}
[WARNING] VISUAL_AGENT: >>> HITL REQUIRED: OTP DETECTED <<<
[USER INPUT REQUIRED] Enter the AppFolio OTP Code: 205026
...
[INFO] VISUAL_AGENT: [Act] Login Complete. Dashboard Detected.
[INFO] VISUAL_AGENT: Session Saved.
```

### Artifacts (Cookies)
The session was successfully persisted to `storage/cookies/appfolio.json`.
```text
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          2/4/2026  10:03 AM           5658 appfolio.json
```

## 3. Security Hardening (Sealing)
To ensure compliance with GitHub Secret Scanning and Enterprise Security Standards, the following changes were applied *after* functional verification but *before* the final push:
-   **Credential Isolation**: Modified `visual_login_agent.py` to strictly require `EMAIL_USER` and `EMAIL_PASS` environment variables (removed hardcoded fallbacks).
-   **Artifact Hygiene**: Updated `.gitignore` to exclude `storage/cookies/*.json`, debug images (`*.jpg`, `*.png`), and page dumps.
-   **History Scrubbing**: Cleaned the commit history to ensure no secrets were accidentally staged.


## 4. Re-Verification (Post-Security Hardening)
Following the security updates (removing hardcoded info), a **Full Re-Run** was conducted to ensure functionality remained intact.
-   **Date**: 2026-02-04 10:41 AM
-   **Method**: `run_visual_agent.ps1` (Env Vars Only).
-   **Result**:
    -   Agent Logged In.
    -   Agent Triggered MFA.
    -   Agent Accepted OTP (`120281`).
    -   Agent Saved Session Cookies.
-   **Status**: **SEALED & VERIFIED**.

## 5. Conclusion
The **VTE System** now possesses an **Intelligent Agent Runtime** capable of handling non-deterministic UI flows. This is a critical milestone for robust "Headless" operations that can still ask for help when needed.
