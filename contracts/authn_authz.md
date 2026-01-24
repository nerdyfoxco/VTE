# VTE AuthN / AuthZ Policy
**Enforcement**: Strict

## 1. Authentication (AuthN)
*   **Primary Identity Provider**: AWS Cognito / Auth0 (OIDC Standard).
*   **Session Management**: Short-lived Access Tokens (1 hour), Rotate Refresh Tokens.
*   **MFA**: Mandatory for `admin` and `auditor` roles.

## 2. Authorization (AuthZ)
*   **Model**: RBAC (Role-Based Access Control) + ABAC (Attribute-Based for Tenancy).
*   **Roles**:
    *   `super_admin`: System Config (Cannot see PII).
    *   `admin`: Tenant Admin (Can see PII if Justified).
    *   `user`: Standard Operations.
    *   `auditor`: Read-Only (Global Scope).
    *   `system_bot`: API Integrations (Scoped).

## 3. Step-Up Authentication
*   **Trigger**: Accessing `irreversible_actions` registry items.
*   **Mechanism**: Re-challenge for password + MFA code.
*   **Timeout**: Step-up validity lasts 5 minutes or Single Action.
