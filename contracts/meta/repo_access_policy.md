# VTE Repository Access & Governance Policy v1.0

## 1. Branch Protection Strategy
To ensure the integrity of the Proof Spine and prevent unverified code from reaching production, the following branch protection rules are enforced on `main` and `release/*` branches.

### 1.1 Protected Branches
- **`main`**: The "working truth". Must always be compilable.
- **`release/v*`**: The "shipped truth". Immutable except for hotfixes via cherry-pick.

### 1.2 Enforcement Rules
- **Require Pull Request Reviews**: Minimum 1 approval from `CODEOWNERS` (Spine or Meta team).
- **Require Status Checks to Pass**:
  - `check_readiness_graph_complete.py`
  - `check_execution_backlog_integrity.py`
  - `prove_bundle_hash_stable_and_matches_sources.py`
  - `prove_unattested_image_blocked_by_admission_controller.py`
- **Require Signed Commits**: All commits must be GPG signed to verify authorship.
- **No Force Pushes**: History rewriting is strictly forbidden on protected branches.

## 2. CI/CD Authentication & Secrets
Access to the repository and deployment environments is governed by the principle of least privilege.

### 2.1 CI Agents
- **Read-Only Default**: CI agents use a Read-Only Deploy Key by default.
- **Write Access**: Restricted to specific "Release Bots" that can only push to `release/*` tags or upload artifacts to the worm-storage.
- **Secret Injection**: Secrets are injected via OIDC (e.g., GitHub Actions OIDC) where possible, avoiding long-lived keys.

### 2.2 Developer Access
- **Write Access**: Developers have write access to `feature/*` and `fix/*` namespaces.
- **Merge Access**: Restricted to Tech Leads and Principals.
- **Admin Access**: Restricted to 2 designated "Break Glass" admins.

## 3. Automation Identity
All automated changes (e.g., from the Agentic Assistant) must be performed under a specific identity.
- **Identity**: `antigravity-bot`
- **Scope**: Limited to proposing changes via PR.
- **Approval**: Automation PRs require human review (HITL) unless explicitly whitelisted by `contracts/meta/change_budget_policy.json`.
