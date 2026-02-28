# Technical Architecture & Core Stack

## 1. Technical Architecture / Tech Stack
The Assistants Platform utilizes the **Canonical UMP Spine-and-Organs Architecture** backed by a strict Model-View-Controller isolation.

### Technology Stack Mapping
*   **Frontend (Eyes & UI):** Next.js 15 (React), Tailwind CSS, Framer Motion for micro-animations.
*   **Backend (Spine & Kidney/Heart):** Python (FastAPI) & Node.js orchestration routines.
*   **Data Persistence:** PostgreSQL managed heavily via Prisma ORM for type safety and enforced relational correctness.

### 1.1 Locate Technology Stack Mismatch & Resolution
A core challenge is running a complex backend agentic engine across disparate client surfaces.
*   **How does it work for Web?**
    The web client uses Next.js server-side rendering combined with client-side hydration. Web apps communicate with the Spine purely over HTTP REST + WebSocket pipes for real-time trace telemetry. Cross-Origin validation and strict JWT auth are enforced.
*   **How does it work for iOS & Android?**
    The platform mitigates native code divergence by utilizing Progressive Web App (PWA) manifesting combined with React Native Web or direct responsive wrappers, ensuring the "Apple-level" UI design language maps identically without separate codebase fragmentation. All heavy compute is strictly server-side; the mobile client is merely a rendering surface.
*   **How does it work for Windows & MacOS?**
    Native OS capabilities (filesystem access, local network) are decoupled. Desktop users consume the engine via the Web surface or a packaged desktop wrapper (Electron/Tauri) mapping strictly to identical cloud REST APIs.
*   **Multi Browser Cloud Bridge:**
    Native execution environments are sandboxed. The AI Agent utilizes explicit cloud browser instances (via Playwright or similar tooling) tied to `start@nerdyfox.co` or `ashim.khanna.cv@gmail.com` to bridge internal functionality to external websites without installing local client executables.

### 1.2 Vector Database Alignment
For the "Brain" and "Organ" contextual memory (LLMO / AI embeddings), Postgres is leveraged directly via the `pgvector` extension.
*   **Rationale:** Using `db.prisma.io` with Postgres vectors eliminates the need for an external DB (like Pinecone) during the initial scale. The system embeds documents, customer journey histories, and scripts (e.g., Anchor Realty data) natively beside transactional data, making Relational + Vector joins (Hybrid Search) seamless and atomic.

## 2. Layers & Relational Tables
The database layer is dictated by Prisma schema files mapped directly to "Ultra Micro Phases" (UMPs).

*   **Tables:** 
    *   `Tenant`, `ExecutionTrace`, `WorkItem`, `IdempotencyLedger`, `AgentSession`, `User`.
*   **Layers:**
    *   **Data Plane (Prisma/DB):** Strict referential integrity.
    *   **Logic Plane (Organs):** Brain, Heart, Lungs, Kidneys validating and orchestrating.
    *   **Transport Plane (Spine/Pipes):** Validated JSON schemas passed via rigid event boundaries.

## 3. The Login Journey
Login mechanisms are heavily restricted to reduce attack surfaces.
*   **Google OAuth:** Configured via `Bryan@assistantscompany.com` GCP console. End-to-end testing utilizes `ashim.khanna.cv@gmail.com`. The flow relies on the `/api/auth/callback/google` endpoint.
*   **Outlook Entra:** B2C and Enterprise Auth mapped via Azure using `vintageorirings@outlook.com`.
*   Users **cannot** sign up using arbitrary username/password methods. Only robust IdP flows are permitted.

## 4. Visual & Interaction Architecture
*   **Calm, Confident, Meaningful:** UI paradigms follow an Apple-native design feel. High use of negative space, soft shadows, typography (Inter/SF Pro), and non-intrusive alerts.
*   **Non-Frozen Interactions:** All buttons, page transitions, and data-fetch actions emit loading states (spinners, skeletons) or micro-animations. A "frozen" UI implies an Error state.
*   **Responsive Default:** Every view—from the complex tracing dashboard to a simple settings page—is fluidly responsive down to 320px width limits. Visually tested by AI agents.

## 5. Hosting & Infrastructure
*   **Azure Hosting:** Utilizing `teams@assistantsco.com`. Note: *Not authorized to upgrade to Pay-as-you-go*. Free/standard tier boundaries strictly monitored by "Economic Control" constraints in the UMP.
*   **AWS / Render / Vercel:** Backup clustering and edge caching. Frontends map to Vercel connected to GitHub (`start@nerdyfox.co`).
*   **Docker:** E2E Containerization. The entire stack (Backend, DB proxies, frontend, worker legs) is built on Docker using `start@nerdyfox.co` Hub accounts. Kubernetes cluster specs maintained inside `/environments/prod/k8s/`.

## 6. API Documentation
*   Follows OpenAPI v3 specs strictly encoded into the Next.js and FastAPI routes.
*   All routes are authenticated, versioned (e.g. `/api/v1/...`), and idempotent via dependency injection headers (`X-Idempotency-Key`).
