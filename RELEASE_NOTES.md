# VTE Release Notes - v1.0.0 (Canonical Foundation)

**Release Date**: 2026-02-27
**Focus**: Master PRD Generation & Strangler Fig Phase 1 Foundation

## 🚀 Key Features
*   **Master PRD Specifications**: Generated exhaustive documentation defining the Canonical UMP Architecture, Operations, SaaS Readiness, and UI/UX execution plans in the `MarkDown Files/` directory.
*   **Canonical UMP System Initialization**: Began the Strangler Fig rollout under `canonical-ump-system/`.
*   **Strict Multi-Tenancy DB**: Deployed `schema.prisma` with explicit Tenant isolation, Workflows, Execution Traces, and Operator Approval tracking.
*   **Command Authority Firewall**: Engineered the sync RBAC/JWT evaluation logic for the orchestration layers (`security/firewall.ts`).
*   **Isolated CI/CD**: Established standalone Dockerfile and GitHub Action workflows for the canonical architecture.

---

# VTE Release Notes - v0.9.0 (RC1)
*   **Unified Queue Dashboard**: "Kevin's Work Day" UI fully implemented with live backend binding.
*   **Visual Agent Surface**: Dedicated `/agent/headless` route for automation stability.
*   **Security Envelopes**:
    *   **Bundle-Only Execution**: Runtime rejects ad-hoc file reads.
    *   **Concurrency Guard**: Global/Tenant limits enforced (1000/100).
*   **Governance**:
    *   **Dual Approval**: Super Admin actions (`IMPERSONATE`) require secondary approver.
*   **Observability**:
    *   **JSON Logs**: Structured logging with PII redaction.
    *   **Incident Timeline**: Standardized post-mortem export.

## 🧪 Verification
The following test suites are passed and integrated into CI:
*   `tests/verify_layer4_backend_logic.py`
*   `tests/verify_layer4_bundle_loader.py`
*   `tests/verify_layer5_concurrency.py`
*   `tests/verify_layer8_observability.py`
*   `tests/verify_layer9_admin.py`
*   **E2E**: Browser automation verified UI/Headless surfaces.

## 📦 Deployment Instructions
1.  **Build**: `docker build -t vte/spine:rc1 .`
2.  **Deploy**: Apply `infrastructure/terraform` (see Layer 5).
3.  **Boot**: Ensure `BundleLoader` has access to signed contracts.

## ⚠️ Known Limitations
*   Auth is currently Mock/Header based (L10 Pending).
*   Egress rules (L6) dependent on Cloud Provider config.
