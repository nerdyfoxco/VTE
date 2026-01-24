# VTE Privacy Policy Implementation
**Compliance Targets**: GDPR, CCPA, Apple App Store Privacy Details

## 1. Data Collection & Purpose
| Data Element | Purpose | Retention |
|--------------|---------|-----------|
| User ID | Identification | 7 Years (Audit) |
| Transaction Amt | Service Core | 7 Years (Audit) |
| IP Address | Security (Fraud) | 30 Days |
| Device ID | Security (Binding) | 7 Years |

## 2. DSAR (Data Subject Access Request) Workflow
1.  **Ingest**: User submits DSAR via Web/Mobile Support.
2.  **Verify**: Support Agent validates identity (Step-Up).
3.  **Execute**:
    *   `export_user_data.py` generates JSON bundle of all `decision_objects` and `evidence`.
    *   (Delete Request) `mark_user_deleted.py` scrubs PII from `actor` columns, replaces with `DELETED_USER_UUID`.
    *   **Note**: Ledger rows are NOT deleted, but anonymized to preserve integrity.

## 3. Privacy Impact Assessment (PIA)
*   **Risk**: High (Financial Data).
*   **Mitigation**: `tenant_isolation`, `encryption_at_rest`, `minimal_collection`.
