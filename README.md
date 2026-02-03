# VTE: Vertical Transaction Engine

![Build Status](https://github.com/nerdyfoxco/VTE/actions/workflows/vte-ci.yaml/badge.svg)
![Security Scan](https://github.com/nerdyfoxco/VTE/actions/workflows/codeql.yaml/badge.svg)
![Docs](https://github.com/nerdyfoxco/VTE/actions/workflows/pages.yaml/badge.svg)

**VTE** is a high-assurance, contract-driven SaaS platform designed for complex vertical transaction management. It features a "Fail-Closed" architecture, ensuring security and data integrity at every layer.

## 🏗 Architecture

The repository allows for a Monorepo structure:

*   **`apps/backend-core` (Spine)**: Python/FastAPI backend using the Canon/Spine architecture.
*   **`apps/frontend` (Web)**: Next.js 15 application with Tier 1 UI/UX.
*   **`contracts/`**: JSON/Markdown definitions that serve as the "Source of Truth" for the system.
*   **`infrastructure/`**: Terraform and Cloud definitions (GitHub Native).

## 🚀 Getting Started

### Prerequisites
*   Node.js v20+
*   Python 3.12+
*   Poetry
*   Docker (Optional, for local env)

### Local Development
1.  **Clone** the repository.
2.  **Install Dependencies**:
    ```bash
    # Backend
    cd apps/backend-core
    poetry install

    # Frontend
    cd apps/frontend
    npm ci
    ```
3.  **Run Development Servers**: (Use separate terminals)
    ```bash
    # Backend
    python tools/debug_uvicorn_spine.py

    # Frontend
    npm run dev
    ```

### ☁️ Codespaces
This repository is fully configured for **GitHub Codespaces**.
Click the **Code** button -> **Codespaces** -> **Create codespace on main** to get a fully pre-provisioned environment.

## 🛡 Governance

*   **Security**: See [SECURITY.md](.github/SECURITY.md) for reporting vulnerabilities.
*   **Contributing**: All changes must go through Pull Requests with passed Status Checks.
*   **Deployments**: deployments to `production` are gated by environment protection rules.

## 📄 Documentation

Full documentation is available at [nerdyfoxco.github.io/VTE](https://nerdyfoxco.github.io/VTE).
