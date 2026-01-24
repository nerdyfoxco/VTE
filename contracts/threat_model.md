# VTE Threat Model (STRIDE)
**Version**: 1.0
**Status**: DRAFT

## 1. Spoofing
*   **Risk**: Attacker impersonates a valid user to submit false decisions.
*   **Mitigation**: OIDC + MFA Enforcement. API validates signature of JWT against IDP Keys.
*   **Residual Risk**: Compromised IDP (Acceptable Risk: Trusted IDP Vendor).

## 2. Tampering
*   **Risk**: DB Administrator modifies `decision_objects` table to erase evidence.
*   **Mitigation**: DB Triggers `prevent_update_delete`. WORM Storage for evidence.
*   **Residual Risk**: Root access to physical disk. (Acceptable Risk: Cloud Provider Physical Security).

## 3. Repudiation
*   **Risk**: User claims they never signed an action.
*   **Mitigation**: `ui_signature` + `permit_token` non-repudiation logs.
*   **Residual Risk**: Client-side malware hijacking session. (Mitigation: Device Binding/Step-Up).

## 4. Information Disclosure
*   **Risk**: Sensitive PII/Evidence leaked to unauthorized tenant.
*   **Mitigation**: RLS (Row Level Security) + Tenant Isolation Policy.

## 5. Denial of Service
*   **Risk**: Api spam exhausts DB connections.
*   **Mitigation**: Rate Limiting (Circuit Breaker) + scalable Postgres Pool.

## 6. Elevation of Privilege
*   **Risk**: Agent tries to promote itself to Admin.
*   **Mitigation**: Hardcoded `no_ai_zones` preventing modification of RBAC tables.
