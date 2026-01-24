# VTE Atomicity & Partial Failure Strategy
**Goal**: Ensure zero partial state application. A decision is either FULLY executed or FULLY rolled back.

## 1. The Atomic Core
The VTE Spine uses **ACID Database Transactions** as the primary synchronization primitive. 
*   **Rule**: A `decision_object` row and its associated `permit_token` MUST be committed in the same DB transaction.

## 2. The Two-Phase Commit (Simulated)
For actions requiring external side-effects (e.g., Stripe Charge + DB Record):
1.  **Phase 1 (Prepare)**: Record `intent` in DB with status `PENDING`.
2.  **Phase 2 (Execute)**: Call External API.
    *   **Success**: Update DB to `APPROVED`.
    *   **Failure**: Update DB to `DENIED` (or `RETRY` if transient).
    *   **Crash during Phase 2**: The `Pending Decision Monitor` (background job) detects stale PENDING state and triggers **Compensation**.

## 3. Handling Crashes
*   **Safe Failure**: If the Spine crashes before DB commit, no record exists. The client retries.
*   **Unsafe Failure**: If Spine crashes AFTER external call but BEFORE DB commit.
    *   **Mitigation**: Idempotency Keys on External APIs. The Recovery Job replays the request; the external provider handles the duplicate.
