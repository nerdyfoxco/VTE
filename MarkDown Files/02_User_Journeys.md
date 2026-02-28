# User Stories & Journey Maps

## 1. Core Operating Principle: Human In The Loop (HITL)
**Rule:** *Where the Human is Required, Always use the AI Agent with a Browser. You always have Explicit Approval.*
The VTE platform flips traditional UX. Humans do not drive the platform; the AI Agent drives, and humans supervise, configure, or break-glass override.

### Human in the Loop Stories / Journey Maps
*   **Trigger:** The AI "Brain" organ hits an abstention threshold (e.g., OCR confidence is <70%, or a tenant pushes back on a complex legal issue).
*   **Journey:** The AI pauses execution. It packages the state into an Actionable Card in the Human Operator Dashboard. The human sees the proposed action, the system confidence, and the verbatim input. The human clicks "Approve", "Modify & Approve", or "Terminate".
*   **Outcome:** The AI resumes via the designated specific browser agent thread using the explicit approval flag context.

## 2. AI Stories / AI Journey
*   **Trigger:** A new email (e.g., from AppFolio or a tenant) enters the Ingestion (Eyes) pipe.
*   **Journey:** 
    1.  *Eyes* parse payload to structured JSON.
    2.  *Kidneys* validate the payload for safety and compliance.
    3.  *Spine* routes it to the *Brain*.
    4.  *Brain* queries context (Vector Postgres DB) and decides the next action (e.g., "Send standard rent overdue SMS").
    5.  *Hands* execute explicitly via internal APIs or Multi-Browser Cloud Bridge agents.
*   **Outcome:** Trace logs are generated and state is committed.

## 3. Personnel Journeys
### Customer Support Stories / Journey
*   **Goal:** Resolve tenant disputes efficiently.
*   **Journey:** Customer Support accesses a "Calm" Dashboard view. Instead of reading raw JSON logs, the system synthesizes the entire tenant interaction thread (Emails, SMS, AI logic traces) into a human-readable case file. Support agents act as the HITL for complex, non-standard lease questions, responding through the VTE platform which dispatches the message down the correct vendor API (e.g., RingCentral).

### Sales Agent Stories / Journey Maps
*   **Goal:** Onboard new property portfolios.
*   **Journey:** Sales uses a distinct portal to configure "Client Configuration Profiles" (similar to Anchor Realty profile). They define grace periods, POC emails, and strike limits. The intuitive UI ensures they map business logic directly into the AI's boundaries without requiring coding.

### Trial Owner / New User - Journey & Story
*   **Goal:** Prove the platform's value within 7 days.
*   **Journey:** Logs in via Google OAuth. The platform provisions a sandboxed "Shadow Execution Engine". The Trial user uploads a sample ledger. The AI generates proposed actions but does *not* execute them (Fail-Closed Sandbox). The user reviews the dashboard, verifying the AI's competency, achieving an "Aha!" moment of trust before enabling live hands.

### Workspace Admin - Journey & Story
*   **Goal:** Manage teams, API limits, and billing.
*   **Journey:** Binds external service credentials (OAuth for AppFolio, Google, AWS). Monitors "Economic Kill Switches" preventing token usage spikes. Assigns role-based access to Team Leads vs Standard Operators.

### Team Lead / Approver - Journey & Story
*   **Goal:** Quality assurance and irreversible action gating.
*   **Journey:** Dashboard filtered primarily for "High Risk / Irreversible" tasks (e.g.. Eviction Notice Approval, Large Refund Approval). Employs bulk-approve/reject patterns.

### Compliance Officer - Journey & Story
*   **Goal:** Ensure HIPAA, SOC2, and Legal Policy adherence.
*   **Journey:** Accesses the read-only Immutable Audit Ledger. Every AI or Human action has a cryptographically hashed receipt with exact decision logic and time-stamps. Ensures no PII leaks outside boundary walls.

### Engineering / Developer (internal) - Journey & Story
*   **Goal:** Debug, trace, and release new UMP chapters.
*   **Journey:** Interacts primarily through Git/GitHub Actions via `start@nerdyfox.co`. Views deep deterministic traces and JSON state graphs. Deploys using the Canonical Pipeline rules—sealing UMPs and avoiding cross-module breaks.

## 4. Multi Browser Cloud Bridge
For APIs that don't exist, the multi-browser cloud bridge journey maps headless Playwright instances. The AI creates isolated incognito sessions, utilizes secure credentials stored in Azure KeyVault/Env vars, navigates target DOMs, performs necessary clicking/scraping (mimicking the "See -> Think -> Act" loop), and closes the session, passing structured JSON back to the Spine.
