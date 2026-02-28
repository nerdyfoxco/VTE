import { evaluatePolicy } from '../rules/evaluator';
import { logEvaluation } from '../observability/logger';
import crypto from 'node:crypto';

export function handlePolicyEvaluatePipe(evaluatePayload: any) {
    const { policy_id, context, requester } = evaluatePayload.data;
    const originalEventId = evaluatePayload.meta.event_id;

    try {
        const result = evaluatePolicy(policy_id, context);

        // Log through Kidney / PII Redaction
        logEvaluation(policy_id, result, context);

        // Emit Output Payload matching `pipe.policy.evaluated.v1`
        return {
            meta: {
                event_id: crypto.randomUUID(),
                timestamp_utc: new Date().toISOString(),
                correlation_id: evaluatePayload.meta.correlation_id,
                producer: 'topic-policy-engine',
                schema_version: '1.0.0'
            },
            data: {
                original_event_id: originalEventId,
                policy_id,
                passed: result.passed,
                reason: result.reason
            }
        };
    } catch (error: any) {
        return {
            error: error.message,
            policy_id
        };
    }
}
