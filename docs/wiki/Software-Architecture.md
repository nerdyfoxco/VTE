# Software Architecture

VTE follows a **Digital Assembly Line** architecture, separating concerns into distinct stages of ingestion, processing, and verification.

## 🧠 The Spine (Backend)
Located in `/apps/backend-core`.
*   **Framework**: FastAPI (Python).
*   **Role**: The "Proof Authority". It holds the truth.
*   **Key Components**:
    *   `contracts/`: JSON Schemas defining Valid Data.
    *   `engine/`: The execution logic (Ingest -> Verify -> Act).
    *   `security/`: OIDC & Role-Based Access Control (RBAC).

## 💻 The Web (Frontend)
Located in `/apps/frontend`.
*   **Framework**: Next.js (React).
*   **Role**: The "View" into the Truth.
*   **Key Components**:
    *   `src/components`: Atomic UI elements.
    *   `src/hooks`: Data fetching and state management.
    *   **Binding**: Automatically generated TypeScript types from Backend Contracts.

## 🏗️ Infrastructure
Located in `/infrastructure`.
*   **Tool**: Terraform.
*   **Registry**: GitHub Container Registry (GHCR).
*   **Scanning**: CodeQL (Static Analysis).

## 🔄 CI/CD Pipeline
Defined in `.github/workflows`.
1.  **Commit**: Code pushed to feature branch.
2.  **Verify**:
    *   `backend-verification`: Pytest, Lint.
    *   `frontend-verification`: Build, Lint.
    *   `Analyze`: CodeQL Security Scan.
3.  **Merge**: Only allowed if all above passed.
4.  **Deploy**:
    *   `vte-deploy`: Builds Docker Image -> Pushes to GHCR.
    *   `pages`: Deploys Docs to GitHub Pages.
