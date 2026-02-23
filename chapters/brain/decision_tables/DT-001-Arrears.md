# Arrears Eligibility Gates

| ArrearsAmount | MoveInDate | Decision | ReasonCode |
| ------------- | ---------- | -------- | ---------- |
| > 10.00       | < 30_DAYS  | HOLD     | NEW_TENANT_GRACE |
| <= 10.00      | ANY        | STOP     | DUST_BALANCE |
| > 10.00       | > 30_DAYS  | APPROVED | CLEAR_TO_CONTACT |

# Compliance Tags
| Tags | Decision | ReasonCode |
| ---- | -------- | ---------- |
| DNC  | STOP     | LEGAL_DNC  |
| JBA  | HOLD     | COURT_ORDER_REVIEW |
