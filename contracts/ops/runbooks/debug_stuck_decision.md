# VTE Runbook: Diagnosing Stuck Decisions (RB-001)

**Trigger**: Ticket from User "My decision is pending for > 1 hour".

## 1. Locate Trace
Query the `decision_objects` table (or Dashboard) using the `decision_id`.
*   Note the `trace_id`.

## 2. Inspect Debug Context
Use the Operator Console to fetch the `decision_trace`.
*   Check `step_latencies_ms`. If one step is > 30s, it timed out.
*   Check `rule_hit_list`. If "MANUAL_REVIEW_REQUIRED" is present, check the HITL Queue.

## 3. Resolution
*   **Timeout**: Retry the decision (Idempotency Key required).
*   **HITL**: Message the `#hitl-ops` channel.
*   **System Error**: Escalate to Engineering with `stack_trace_hash`.
