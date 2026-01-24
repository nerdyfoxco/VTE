# VTE Risk Acceptance Register
**Status**: ACTIVE

This document tracks all known deviations from the strict Security & Operational standards. Each item acts as a temporary "waiver" and must have a resolution plan.

| Risk ID | Description | Severity | Justification | Approver | Expiration Date |
|---------|-------------|----------|---------------|----------|-----------------|
| RISK-001 | **Sync DB Driver in Async API** | MEDIUM | `psycopg2` is stable; `asyncpg` migration planned for Phase 2. Blocking I/O limited by connection pool. | @tech_lead | 2026-06-01 |
| RISK-002 | **Stubbed DAST Tool** | LOW | Commercial DAST (Burp/ZAP) integration pending budget approval. Baseline check covers headers. | @security_mgr | 2026-03-01 |
| RISK-003 | **Mocked Identity Provider** | HIGH | Local Dev uses fake OIDC issuer. Production MUST use AWS Cognito. | @architect | 2026-02-01 |
