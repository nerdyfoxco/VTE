# SaaS Deployability Gap Analysis

While the current PRD suite defines the core engine, UI/UX, and execution model, transitioning from a robust "Engine" to a commercial **SaaS Deployable Project** requires several operational, financial, and compliance layers. 

Here is the analysis of what is currently missing to make this a fully shippable SaaS product:

## 1. Billing, Monetization & Metering
The platform orchestrates complex AI actions and browser instances, which carry variable costs (LLM tokens, compute time).
*   **Gap:** No defined subscription tiers, payment gateway integration, or usage metering.
*   **SaaS Requirement:**
    *   Integration with a billing provider (e.g., Stripe) for subscription management.
    *   **Usage-Based Billing:** A ledger to track API calls and LLM token usage per tenant to enforce the "Economic Kill Switches" and bill appropriately.
    *   Feature-gating mechanisms based on subscription tiers (e.g., Trial vs. Pro vs. Enterprise).

## 2. Strict Multi-Tenancy Data Isolation
While the architecture mentions tenant quotas, the exact database strategy for keeping multiple clients' data completely isolated is undefined.
*   **Gap:** Ambiguity on whether Prisma/Postgres relies on Application-Level filtering, Row-Level Security (RLS), or isolated database schemas.
*   **SaaS Requirement:**
    *   Explicit Row-Level Security (RLS) policies defined in Postgres to mathematically guarantee that Tenant A cannot query Tenant B's Execution Traces, even if the application logic fails.
    *   Secure tenant onboarding and offboarding workflows (data purging).

## 3. Observability, APM, and SLAs
A production SaaS needs zero-blind-spot visibility.
*   **Gap:** The infrastructure relies on logging, but lacks an APM (Application Performance Monitoring) strategy.
*   **SaaS Requirement:**
    *   Integration with OpenTelemetry, DataDog, or Sentry for distributed tracing across the Next.js frontend, Python Spine, and Playwright browsers.
    *   Public Status Page infrastructure to communicate uptime.
    *   Defined Service Level Agreements (SLAs) and automated paging (e.g., PagerDuty) when the backend or "Spine" drops.

## 4. Security Operations (SecOps) & Compliance
B2B SaaS platforms selling to property management or financial sectors require strict compliance.
*   **Gap:** Missing WAF layers and explicit compliance attestation strategies.
*   **SaaS Requirement:**
    *   **WAF (Web Application Firewall):** Configuration via Cloudflare or Azure/AWS WAF to prevent DDoS, SQLi, and bot attacks before they hit the Next.js edge.
    *   **Secret Orchestration:** Strict definition of how API keys (OpenAI, AppFolio, Stripe) are injected into the runtime without sitting in plaintext environment files.
    *   **GDPR / CCPA:** Explicit endpoints for "Right to be Forgotten" that scrub a human from the Vector DB and relational tables smoothly.

## 5. Support Ecosystem & Knowledge Base
The PRD defines the *Customer Support Persona*, but not the tooling they use to interact with the SaaS users.
*   **Gap:** No CRM/Ticketing system for external user support.
*   **SaaS Requirement:**
    *   Integration with Intercom, Zendesk, or HubSpot to catch user bug reports or feature requests directly from the web application.
    *   A public-facing Knowledge Base / Help Center (e.g., GitBook or standard Next.js docs).

## 6. Disaster Recovery & Backups
*   **Gap:** What happens if the primary Postgres cluster goes down?
*   **SaaS Requirement:**
    *   Point-in-Time Recovery (PITR) enabled on the Postgres cluster.
    *   Defined RTO (Recovery Time Objective) and RPO (Recovery Point Objective).
    *   Multi-region or availability-zone failover definitions inside the Kubernetes/Azure topologies.

## 7. Automated Onboarding & Data Migration
A true SaaS product needs self-serve onboarding, especially when handling complex client data.
*   **Gap:** No automated pipeline for a new property management company to migrate their historical data.
*   **SaaS Requirement:**
    *   Self-serve CSV/Excel upload portals with automated schema mapping.
    *   OAuth-driven API syncing (e.g., clicking "Connect AppFolio" and having the AI automatically pull the last 90 days of ledgers).

## 8. Role-Based Access Control (RBAC) & Governance UI
While the architecture defines the roles (Admin, Approver), the configuration UI for these roles is missing.
*   **Gap:** No administration console for clients to manage their own team's permissions.
*   **SaaS Requirement:**
    *   A Workspace Administration panel allowing the "Super Admin" to set approval thresholds (e.g., "Any action over $500 requires Team Lead approval").
    *   Granular API key generation for clients who want to integrate the VTE into their own internal tools.

## 9. Comprehensive Audit Logging & Export (SOC2/HIPAA)
Clients in regulated industries require proof of everything the system does.
*   **Gap:** The Execution Traces exist internally, but there is no client-facing export mechanism.
*   **SaaS Requirement:**
    *   Immutable audit logs accessible via the UI.
    *   One-click export to CSV/PDF for compliance reporting.
    *   Integration with external SIEM tools (e.g., Splunk, Datadog) for enterprise clients.

## 10. Webhooks & Developer API (Outbound)
B2B clients will not always live in your UI; they want your system to talk to their systems.
*   **Gap:** No outbound event notification system.
*   **SaaS Requirement:**
    *   A Webhook registry where clients can subscribe to events (e.g., `workflow.completed`, `hitl.required`).
    *   A public-facing REST/GraphQL API documented with Swagger/OpenAPI for clients to trigger agents programmatically.

## 11. Legal, Licensing, & Terms of Service (ToS)
*   **Gap:** No legal guardrails around AI execution liability.
*   **SaaS Requirement:**
    *   Clickwrap agreements blocking access until ToS and Privacy Policies are accepted.
    *   Clear legal boundaries defining a "Shared Responsibility Model" (e.g., who is liable if the AI drafts an incorrect email, versus if the human explicitly approves it).
    *   Custom domain mapping and white-labeling capabilities for enterprise clients.

## Conclusion
To cross the boundary from "High-Assurance Engineering Project" to a mature "B2B SaaS Business," we must instantiate the **Billing Engine**, configure **Row-Level Security** in Postgres, layer **SecOps/APM** over the infrastructure, and build the **Self-Serve Onboarding & Governance** portals necessary for true enterprise adoption.
