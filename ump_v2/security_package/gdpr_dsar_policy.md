# GDPR / CCPA Data Subject Access Request (DSAR) Policy

## 1. Overview
The VTE 3.0 Platform enforces a strict "Fail-Closed," append-only architecture. This document outlines the engineering constraints required to fulfill DSAR obligations (Right to Access, Right to be Forgotten) without violating the immutability of the Execution Engine traces.

## 2. Right to Access (Export)
*   **Trigger**: An Operator with the `Auditor` role initiates an export via the API (`/compliance/dsar/export/{user_id}`).
*   **Execution**:
    1.  The system queries the `UserModel` for the physical identity.
    2.  The system queries the `DecisionTraceModel` for all `intent_hashes` linked to the user's `workspace_id`.
    3.  A unified JSON bundle is generated, signed by the system's private key, and placed in a secure, time-limited download bucket.
*   **Format**: Plain JSON. No proprietary binary formats.

## 3. Right to be Forgotten (Redaction vs. Deletion)
*   **Constraint**: The `vte_spine.db` is strictly immutable. Data *cannot* be `DELETE`d via SQL.
*   **Execution (Cryptographic Erasure)**:
    1.  Instead of deleting rows, the PII fields (Name, Email, Phone) within the `UserModel` and associated traces are fundamentally overwritten with a cryptographically secure hash (e.g., `SHA-256(user_id + salt)`).
    2.  The `tenant_id` and the deterministic execution outcome (`HOLD`, `PROCEED`) remain intact for systemic audit integrity.
    3.  The physical key required to re-identify the hash is destroyed.

## 4. Consent Registry Interaction
*   If a DSAR deletion is processed, the user's `ConsentRecordModel` is immediately updated to `consent_granted = FALSE`, instantly triggering a `STOP` propagation across all running VTE State Machines.
*   **Fail-Closed**: Any inbound webhook referencing the erased `user_id` will immediately trigger a `PipeEnvelopeRejectError`.
