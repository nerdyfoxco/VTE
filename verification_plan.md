# E2E Visual Verification Plan: Kevin's Work Cycle

Based on `Kevin Work Cycle.txt`, Kevin's legacy manual workflow required authenticating across multiple platforms (Gmail, AppFolio), comparing massive Google Sheets against AppFolio ledgers, reading complex transaction codes, manually composing multi-channel outreach, and double-entering notes.

VTE (Verified Transaction Execution) is designed to unify and automate this. This document outlines the Phase-wise Objectives, Features, Functions, Expectations, Real-World Use, and Outputs to verify the system End-to-End.

---

## Phase 1: Secure Authentication & Work Initiation
*   **Objective:** Securely log into the unified workspace and establish identity.
*   **Features:** MFA Challenge, Cookie Consent, Global Layout routing.
*   **Functions:** `/login`, `/mfa/verify` APIs; JWT Session storage.
*   **Expectations:** The user encounters the Cookie Consent banner. The user logs in with credentials and is successfully intercepted by the MFA challenge before gaining access.
*   **Real World Use:** Protects PII and financial ledger data by enforcing enterprise-grade identity checks before exposing Kevin's Work Day queue.
*   **Outputs:** Active secure session, redirection to the primary `/dashboard`.

## Phase 2: Ingestion & Triaging (The Unified Queue)
*   **Objective:** Identify actionable tenants without cross-referencing external Google Sheets.
*   **Features:** Kevin's Work Day Dashboard, Live Polling, Keyboard Navigation (j/k/Enter).
*   **Functions:** Fetching and rendering `GET /api/workqueue`.
*   **Expectations:** Kevin sees a clean, prioritized list of delinquent or actionable tenants. He can rapidly move through the list using keyboard shortcuts. The SLA deadlines should be formatted human-readably (e.g., "Due in 2 hours" in red).
*   **Real World Use:** Eliminates the need to copy-paste 60-80 rows from a Delinquency Report into a local Calling List.
*   **Outputs:** A selected, active task row ready for deep dive.

## Phase 3: Contextual Analysis (Evidence Review)
*   **Objective:** Analyze the single source of truth to ensure a tenant *should* be contacted.
*   **Features:** Evidence/Ledger View within the specific Trace.
*   **Functions:** Displaying balances, recent payments, and explicit tags (e.g., DNC, JBA).
*   **Expectations:** Kevin can see the necessary ledger evidence on-screen. If the outstanding balance is solely a new water bill (giving 4-5 days grace) or a DNC tag exists, the system should present this clearly so Kevin can skip.
*   **Real World Use:** Automates the cognitive load of reading the bottom of an Appfolio ledger and decoding complex charge types ("Rent Income - Past Due"). 
*   **Outputs:** A definitive GO/NO-GO decision on outreach.

## Phase 4: Seamless Outreach Execution
*   **Objective:** Execute standardized communication across required channels without platform swapping.
*   **Features:** Action Buttons, Template generation, Email/SMS initiation.
*   **Functions:** Interacting with the actionable item CTA.
*   **Expectations:** Hitting `Enter` or clicking an action triggers the outreach sequence. The system should mimic sending the required template ("This is Kevin from Anchor Realty...").
*   **Real World Use:** Kevin no longer manually types out texts and emails from within AppFolio's buried menus. 
*   **Outputs:** Triggered communication side-effects.

## Phase 5: Fast Resolution & Record Keeping
*   **Objective:** Process the item and log the transaction instantly.
*   **Features:** Optimistic UI Updates, Toast Notifications with Undo.
*   **Functions:** Resolving the queue item state.
*   **Expectations:** The row instantly disappears from the UI upon processing. A Toast notification appears confirming the action (e.g., "Outreach Recorded") and offering a 5-second `Undo` window.
*   **Real World Use:** Eliminates double-entry. Kevin no longer needs to manually write `<PHONE NUMBER> CALL TEXT EMAIL` in AppFolio and then copy that note back to the Google Sheet.
*   **Outputs:** A clean, shrinking queue that seamlessly moves to the next tenant.

---

## Testing Protocol & Automated Tasks
I will perform the following linear verification using the Browser Subagent. For **every phase**:
1. Execute the UI action against the running VTE server.
2. Capture a screenshot of the state.
3. Log the screenshot to `Gaps and Mistakes.md` along with a rigorous analysis identifying any UI errors, backend failures, or security attack vectors.
