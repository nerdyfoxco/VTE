# VTE Implementation Plan: The Single Deterministic Path

## Architectural Lock-In
Per the user's request, we are committing to a Single Deterministic Path to resolve all architectural conflicts immediately.

1. **Unified Tech Stack: 100% Node.js (The UMP System)**. We are fully deprecating the legacy Python `spine` and committing 100% to the `canonical-ump-system` (Node.js, Express, Prisma, TypeScript).
2. **Frontend Strategy: Next.js Web-First**. The Command Center and Data Plane operations will be exclusively built using Next.js (React + TypeScript).
3. **Vector Database: local `pgvector`**. We will utilize `pgvector` tied to Prisma instead of external Pinecone services to guarantee strict tenant isolation and simplify architecture.
4. **Rules Engine: Decision Tables in Postgres**. Tenant-specific policies and SOPs (like "Kevin's Work Day") will be stored as Decision Tables in Postgres, evaluated at runtime, enabling UI-driven "Fail-Closed Determinism".

---

# Strangler Fig Phase 8: Hardening Cross-Boundary Authentication

## 1. Goal Description
To allow the VTE Frontend Dashboard to naturally transition between Legacy Python routes and the new Canonical UMP Native Node.js routes, both platforms must speak the exact same cryptographic language. 

Currently, the legacy Python `/auth/token` endpoint returns development mock tokens (e.g., `fake-jwt-token-USER`), but the strict Node.js `CommandAuthorityFirewall` demands cryptographically valid HS256 JWTs injected with core Multi-Tenancy claims (`tenantId`, `operatorId`, `role`, `email`).

Phase 8 will bridge this gap, authorizing the UI properly across both systems.

## 2. Proposed Changes

### 2a. Python JWT Issuer Maturation
*   [MODIFY] `apps/backend-core/spine/api/routers/auth.py`
    *   Import `jwt` from the `jose` library (already installed).
    *   Replace the fake token string generation with a securely signed HS256 JWT.
    *   Inject the claims strictly required by the Node interface: `{"tenantId": user.tenant_id, "operatorId": user.username, "role": user.role, "email": user.username}`.

### 2b. Node.js Gateway Key Synchronization
*   [MODIFY] `canonical-ump-system/foundation/package.json`
    *   Update the `start:gateway` script to explicitly inject $env:VTE_JWT_SECRET matching the Python configuration before running `tsx src/gateway.ts`.

### 2c. Frontend UI Validation
*   [VERIFY] Start BOTH the Python Server (Port `8001`) and the unified Node Gateway (Port `8000`).
*   [VERIFY] Connect to the frontend UI (`http://localhost:3000`), perform a live Login as an Administrator, and verify the UI successfully retrieves the strangled Queue list from the Node layer.

## 3. Verification Plan
### Automated Tests
*   `curl` the Python login endpoint directly to assert it returns a cleanly decodable 3-part JWT string.
### Manual Verification
*   We will natively browse the frontend application to prove that navigating the Dashboard seamlessly routes Legacy and Strangled traffic using a single unified Token architecture.

---

# Strangler Fig Phase 9: End-to-End Orchestration (Wiring "Process Item")

## 1. Goal Description
Right now, the Frontend Dashboard has `Process Item` buttons that act as placeholders triggering a generic browser `alert()`. To prove the full business value of the new Strangler Fig architecture, we must wire these buttons to spawn traces traversing the `Kidney -> Brain -> Hands` Canonical micro-organs.

## 2. Proposed Changes

### 2a. Expose Live Engine Execution
*   [MODIFY] `canonical-ump-system/chapters/brain/topic-orchestration/src/routes.ts`
    *   Expose a strictly authenticated `POST /api/v1/orchestration/live` REST endpoint.
    *   This API will receive a strictly typed `WorkflowExecutionSchema` payload, assert the user role using the Express middleware, and dispatch the context natively into `shadowEngine.routeInLiveMode()`.

### 2b. Dispatch Live Traces from the Control Plane
*   [MODIFY] `apps/frontend/src/app/page.tsx`
    *   Replace the placeholder `alert()` calls tied to the "Process Item" buttons (Desktop and Mobile map blocks).
    *   Synthesize a strictly-shaped payload corresponding to the target Queue Item ID.
    *   Issue a secure JSON `axios.post` to the new Canonical `/api/v1/orchestration/live` endpoint using the `localStorage` injected JWT.
    *   Upon a `200 OK` response, dynamically update the Queue Item's state in the UI (e.g. marking it as 'Processing...' or reloading the fetch context) while pushing a success Toast to the user mapping the unique Execution Trace ID.

## 3. Verification Plan
### Automated Tests
*   Run the Node Gateway and manually `curl` the `/live` endpoint with a mocked JWT payload to verify side-effect handling and 200 OK responses.
### Manual Verification
*   Connect the Browser Subagent to the Next.js `http://localhost:3000` instance.
*   Log in and visibly click a "Process Item" button inside the UI.
*   Assert that the successful Toast UI notification fires immediately and Network requests confirm successful 200 resolution.

---

# Strangler Fig Phase 10: Initializing Downstream Code Versioning (GitHub)

## 1. Goal Description
To safely persist the entire Canonical UMP framework and the `vte_backend.db` rewrites, we must configure and dispatch local Git modifications securely up to the upstream GitHub remote endpoint. Over 40 files have been introduced in the `canonical-ump-system` directory that need to be explicitly tracked.

## 2. Proposed Changes
*   [EXECUTE] Stage all non-ignored modified or new files resulting from the Strangler Fig rewrite.
*   [EXECUTE] Formulate a single cohesive monolithic commit `feat: Phase 1-9 Strangler Fig Canonical Rewrite` capturing the `canonical-ump-system` structure and frontend/backend integration patches.
*   [EXECUTE] Execute `git push origin feat/canonical-ump-phases-3-5` to align the remote branch.

## 3. Verification Plan
*   Assert that `git status` returns a perfectly clean working tree.
*   Assert the terminal trace output confirming `compressing objects` and successful transmission to `github.com/nerdyfoxco/VTE.git`.

---

# Strangler Fig Phase 11: Real-World Dispatch Integrations (The Hands Module)

# Strangler Fig Phase 8: Hardening Cross-Boundary Authentication

## 1. Goal Description
To allow the VTE Frontend Dashboard to naturally transition between Legacy Python routes and the new Canonical UMP Native Node.js routes, both platforms must speak the exact same cryptographic language. 

Currently, the legacy Python `/auth/token` endpoint returns development mock tokens (e.g., `fake-jwt-token-USER`), but the strict Node.js `CommandAuthorityFirewall` demands cryptographically valid HS256 JWTs injected with core Multi-Tenancy claims (`tenantId`, `operatorId`, `role`, `email`).

Phase 8 will bridge this gap, authorizing the UI properly across both systems.

## 2. Proposed Changes

### 2a. Python JWT Issuer Maturation
*   [MODIFY] `apps/backend-core/spine/api/routers/auth.py`
    *   Import `jwt` from the `jose` library (already installed).
    *   Replace the fake token string generation with a securely signed HS256 JWT.
    *   Inject the claims strictly required by the Node interface: `{"tenantId": user.tenant_id, "operatorId": user.username, "role": user.role, "email": user.username}`.

### 2b. Node.js Gateway Key Synchronization
*   [MODIFY] `canonical-ump-system/foundation/package.json`
    *   Update the `start:gateway` script to explicitly inject $env:VTE_JWT_SECRET matching the Python configuration before running `tsx src/gateway.ts`.

### 2c. Frontend UI Validation
*   [VERIFY] Start BOTH the Python Server (Port `8001`) and the unified Node Gateway (Port `8000`).
*   [VERIFY] Connect to the frontend UI (`http://localhost:3000`), perform a live Login as an Administrator, and verify the UI successfully retrieves the strangled Queue list from the Node layer.

## 3. Verification Plan
### Automated Tests
*   `curl` the Python login endpoint directly to assert it returns a cleanly decodable 3-part JWT string.
### Manual Verification
*   We will natively browse the frontend application to prove that navigating the Dashboard seamlessly routes Legacy and Strangled traffic using a single unified Token architecture.

---

# Strangler Fig Phase 9: End-to-End Orchestration (Wiring "Process Item")

## 1. Goal Description
Right now, the Frontend Dashboard has `Process Item` buttons that act as placeholders triggering a generic browser `alert()`. To prove the full business value of the new Strangler Fig architecture, we must wire these buttons to spawn traces traversing the `Kidney -> Brain -> Hands` Canonical micro-organs.

## 2. Proposed Changes

### 2a. Expose Live Engine Execution
*   [MODIFY] `canonical-ump-system/chapters/brain/topic-orchestration/src/routes.ts`
    *   Expose a strictly authenticated `POST /api/v1/orchestration/live` REST endpoint.
    *   This API will receive a strictly typed `WorkflowExecutionSchema` payload, assert the user role using the Express middleware, and dispatch the context natively into `shadowEngine.routeInLiveMode()`.

### 2b. Dispatch Live Traces from the Control Plane
*   [MODIFY] `apps/frontend/src/app/page.tsx`
    *   Replace the placeholder `alert()` calls tied to the "Process Item" buttons (Desktop and Mobile map blocks).
    *   Synthesize a strictly-shaped payload corresponding to the target Queue Item ID.
    *   Issue a secure JSON `axios.post` to the new Canonical `/api/v1/orchestration/live` endpoint using the `localStorage` injected JWT.
    *   Upon a `200 OK` response, dynamically update the Queue Item's state in the UI (e.g. marking it as 'Processing...' or reloading the fetch context) while pushing a success Toast to the user mapping the unique Execution Trace ID.

## 3. Verification Plan
### Automated Tests
*   Run the Node Gateway and manually `curl` the `/live` endpoint with a mocked JWT payload to verify side-effect handling and 200 OK responses.
### Manual Verification
*   Connect the Browser Subagent to the Next.js `http://localhost:3000` instance.
*   Log in and visibly click a "Process Item" button inside the UI.
*   Assert that the successful Toast UI notification fires immediately and Network requests confirm successful 200 resolution.

---

# Strangler Fig Phase 10: Initializing Downstream Code Versioning (GitHub)

## 1. Goal Description
To safely persist the entire Canonical UMP framework and the `vte_backend.db` rewrites, we must configure and dispatch local Git modifications securely up to the upstream GitHub remote endpoint. Over 40 files have been introduced in the `canonical-ump-system` directory that need to be explicitly tracked.

## 2. Proposed Changes
*   [EXECUTE] Stage all non-ignored modified or new files resulting from the Strangler Fig rewrite.
*   [EXECUTE] Formulate a single cohesive monolithic commit `feat: Phase 1-9 Strangler Fig Canonical Rewrite` capturing the `canonical-ump-system` structure and frontend/backend integration patches.
*   [EXECUTE] Execute `git push origin feat/canonical-ump-phases-3-5` to align the remote branch.

## 3. Verification Plan
*   Assert that `git status` returns a perfectly clean working tree.
*   Assert the terminal trace output confirming `compressing objects` and successful transmission to `github.com/nerdyfoxco/VTE.git`.

---

# Strangler Fig Phase 11: Real-World Dispatch Integrations (The Hands Module)

## 1. Goal Description
Currently, the `SideEffectDispatcher` in the `topic-dispatch` module only logs console messages when simulating external side-effects like "Email Tenant". To fully validate the Canonical UMP framework's utility, we must wire the "Hands" module up to a real-world integrations layer (e.g., SMTP, Gmail API, SendGrid) to prove that the execution engine can perform tangible, deterministic actions.

## 2. Proposed Changes
*   **[MODIFY]** `canonical-ump-system/chapters/hands/topic-dispatch/src/providers/email.ts`
    *   Deprecate the `MockEmailProvider` and replace it with a `LiveEmailProvider`.
    *   Integrate a standard email SDK (like `nodemailer` or an external API based on User preference).
*   **[MODIFY]** `canonical-ump-system/chapters/hands/topic-dispatch/src/dispatcher.ts`
    *   Update the engine's `routeEffect` method to safely instantiate the Live provider, gracefully catching transmission faults.
*   **[NEW]** Setup environmental variables for the API keys or SMTP credentials within the Gateway foundation.

## 3. Verification Plan
*   Connect the User Dashboard through `localhost:3000` via the Browser Subagent.
*   Log in and trigger the `Process Item` orchestration trace on a pending Queue item.
*   Verify the trace is recorded successfully, and assert that the real-world external side-effect (e.g. an email dropping into a test inbox) fires successfully.

---

# Strangler Fig Phase 12: Real Database Migration (SQLite to PostgreSQL)

## 1. Goal Description
The system currently relies on two separated legacy SQLite databases: `vte_backend.db` (Python) and `foundation/prisma/dev.db` (Node.js). Because SQLite is terrible at high-concurrency cross-platform locks and we have to mock referential integrity (like mocking Trace IDs), we must unify both the legacy Python app and the modern Node.js app onto a single, robust PostgreSQL instance via Docker Compose.

## 2. Proposed Changes
*   **[NEW]** `docker-compose.yml` (Root)
    *   Initialize a local `postgres:15-alpine` container for development.
*   **[MODIFY]** `canonical-ump-system/foundation/prisma/schema.prisma`
    *   Switch `provider = "sqlite"` to `"postgresql"`.
    *   Run `npx prisma migrate dev` to generate the new schema locally.
*   **[MODIFY]** `apps/backend-core/spine/vte/db.py` and `alembic.ini`
    *   Update SQLAlchemy connection strings to point to the shared PostgreSQL environment variable.
*   **[MODIFY]** `canonical-ump-system/chapters/brain/topic-orchestration/src/shadow.ts`
    *   Remove the fake mocked `uuidv4()` Trace implementations now that real cross-table foreign keys will succeed within the unified database.

## 3. Verification Plan
*   Run `docker-compose up -d`.
*   Connect Prisma Studio and ensure both old User tables and new Trace tables exist in the same schema.
*   Execute an orchestration trace and verify it natively persists to the PostgreSQL database without constraint exceptions.

---

# Strangler Fig Phase 13: Strangling Authentication & Users (Core Foundation)

## 1. Goal Description
Right now, Python still owns the `users` table and issues the JWTs via the `/auth/token` endpoint. We will natively move user management and authentication directly into the Node.js Foundation, finalizing the retirement of the highest-risk legacy perimeter.

## 2. Proposed Changes
*   **[MODIFY]** `canonical-ump-system/foundation/prisma/schema.prisma`
    *   Bring the `User`, `Tenant`, and `UserSession` models strictly into the Prisma schema.
*   **[NEW]** `canonical-ump-system/foundation/src/auth/`
    *   Construct standard native Express routes inside the Node Foundation for handling User Login, Registration, and Google OAuth payload extraction.
*   **[MODIFY]** `canonical-ump-system/gateway/topic-routing/src/main.ts`
    *   Remove the `http-proxy-middleware` bypass for `/api/v1/auth` and sink it natively down into the new Node.js router.
*   **[MODIFY]** `apps/frontend/src/` (Various fetch layers)
    *   Ensure the frontend dynamically adapts strictly to the Node.js payload structures if any minor differences exist.

## 3. Verification Plan
*   Kill the Python server completely.
*   Launch only the Node.js server.
*   Load the Frontend Dashboard and successfully login with the Admin credentials. If it succeeds, the Auth perimeter has been successfully strangled!

---

# Strangler Fig Phase 14: Strangling Gmail Ingestion (Senses Module)

## 1. Goal Description
Email ingestion historically lives in the Python backend via background polling. We will stand up a new `topic-ingestion` Canonical module underneath the `Senses` organ. This Node.js worker will be responsible for natively connecting to the Google API using the shared `token.json` and directly translating raw emails into Canonical `QueueItem` instances.

## 2. Proposed Changes
*   **[NEW]** `canonical-ump-system/chapters/senses/topic-ingestion/`
    *   Initialize a new Node module with Google API SDK (`googleapis`).
*   **[NEW]** `canonical-ump-system/chapters/senses/topic-ingestion/src/providers/google_mail.ts`
    *   Implement an asynchronous poller that parses the `token.json` file.
    *   Fetch unread messages, parse their headers, and map them to `Prisma.QueueItemCreateInput`.
*   **[MODIFY]** `canonical-ump-system/chapters/brain/topic-orchestration/src/shadow.ts`
    *   Wire the `topic-ingestion` service so that any natively discovered email instantly spawns a new Kidney -> Brain -> Hands evaluation loop.

## 3. Verification Plan
*   Start the node app with the `client_secret.json` and `token.json` actively synced in the root.
*   Send a real live email to the target inbox.
*   Watch the Node.js console log the automated retrieval of the email, the successful insertion into the `QueueItem` database, and the automatic trace completion in Prisma Studio.
