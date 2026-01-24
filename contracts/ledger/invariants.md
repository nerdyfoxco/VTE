# VTE Non-Negotiable Invariant Ledger
**Status**: SEALED
**Enforcement**: STRICT

This document defines the **Immutable Laws** of the Verified Transaction Environment. Violation of any invariant constitutes a catastrophic system failure and must trigger an immediate **Kill Switch**.

## 1. The Law of Immutability
**Invariant 1.1**: History cannot be rewritten.
*   **Requirement**: `decision_objects`, `evidence_bundles`, and `permit_tokens` MUST reside in Append-Only tables protected by `prevent_update_delete()` triggers.
*   **Verification**: DB Schema Audit, Runtime Exception on UPDATE/DELETE attempt.

**Invariant 1.2**: Evidence precedes Decision.
*   **Requirement**: A `decision_object` CANNOT be created without a valid reference to an existing `evidence_bundle` hash (unless Evidence is logically NULL for the intent type, which is restricted).
*   **Verification**: Foreign Key Constraint + Application Logic.

**Invariant 1.3**: Decision precedes Side-Effect.
*   **Requirement**: No side-effect (API call, DB write outside ledger, Email) can occur without a signed `permit_token`.
*   **Verification**: `ProofVerifier` checked in every Connector/Gateway.

## 2. The Law of Identity
**Invariant 2.1**: No Anonymous Actions.
*   **Requirement**: Every `decision_object` must bind to an authenticated `actor_user_id` and specific `actor_role`.
*   **Verification**: API Auth Middleware + Token Introspection.

**Invariant 2.2**: Role Stability.
*   **Requirement**: An actor cannot change roles within the same `decision_chain` segment (Atomic Session).

## 3. The Law of Containment (AI Safety)
**Invariant 3.1**: No Unverified AI Generation.
*   **Requirement**: AI-generated content used as Evidence MUST be labeled `source: "ai_model"` and requires Human-in-the-Loop (HITL) review for Criticality HIGH actions.
*   **Verification**: Content-Type Headers + HITL Queue Logic.

**Invariant 3.2**: No AI Policy Modification.
*   **Requirement**: AI agents cannot modify `policy_version` strings or deployment configurations.
*   **Verification**: `CODEOWNERS` + Protected Branch policies (Agents have no Write access to `contracts/`).

**Invariant 3.3**: The Kill Switch is Absolute.
*   **Requirement**: If `global_kill_switch` is active, 0 traffic flows.
*   **Verification**: Middleware Check on Request Start.

## 4. The Law of Transparency
**Invariant 4.1**: Audit Completeness.
*   **Requirement**: Every system state change must emit a structured log/trace.
*   **Verification**: Observability Pipeline Canary.
