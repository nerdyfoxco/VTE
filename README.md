# VTE: Vertical Transaction Engine

![Build Status](https://github.com/nerdyfoxco/VTE/actions/workflows/vte-ci.yaml/badge.svg)
![Security Scan](https://github.com/nerdyfoxco/VTE/actions/workflows/codeql.yaml/badge.svg)
![Docs](https://github.com/nerdyfoxco/VTE/actions/workflows/pages.yaml/badge.svg)

**VTE** is a high-assurance, contract-driven SaaS platform designed for complex vertical transaction management. It features a "Fail-Closed" architecture, ensuring security and data integrity at every layer.

## 🏗 Architecture

The repository allows for a Monorepo structure moving towards a strict Canonical UMP Model:

*   **`MarkDown Files/`**: The definitive Master Product Requirements Document (PRD) governing all UMP execution.
*   **`canonical-ump-system/`**: The Phase 1 Strangler Fig implementation of the strict API Orchestration and database Foundation.
*   **`apps/backend-core` (Legacy Spine)**: Initial Python/FastAPI backend execution engine.
*   **`apps/frontend` (Web)**: Next.js 15 application with Tier 1 UI/UX.
*   **`contracts/`**: JSON/Markdown definitions that serve as the "Source of Truth" for the system.
*   **`infrastructure/`**: Terraform and Cloud definitions (GitHub Native).

## 📚 Documentation
- **[Project Roadmap](docs/wiki/Roadmap.md)**: The journey from V1 to Enterprise Scale.
- **[Current Status](docs/wiki/Current-Status.md)**: Real-time operational dashboard.
- **[Software Architecture](docs/wiki/Software-Architecture.md)**: Deep dive into Spine & Web.
- **[Full Wiki](docs/wiki/Home.md)**: Improving software, better, together.

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
