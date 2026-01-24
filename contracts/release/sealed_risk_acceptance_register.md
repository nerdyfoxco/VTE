# Sealed Risk Acceptance Register

| Risk ID | Description | Accepted By | Date | Signature |
| :--- | :--- | :--- | :--- | :--- |
| RISK-001 | Legacy DB connection does not support TLS 1.3 (Uses 1.2) | CTO | 2026-01-23 | *signed:cto_key* |
| RISK-002 | Email provider lacks region affinity | CISO | 2026-01-23 | *signed:ciso_key* |

**Policy:**
1. All known risks MUST be listed here.
2. Deployment Gate MUST fail if an active risk is detected that is NOT in this register.
