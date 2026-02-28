import { redactContext } from '../../../../../foundation/src/security/redact';
import { PolicyResult } from '../rules/evaluator';

export function logEvaluation(policyId: string, result: PolicyResult, context: Record<string, any>): void {
    const safeContext = redactContext(context);

    const logEntry = {
        eventType: 'POLICY_EVALUATION',
        timestamp: new Date().toISOString(),
        policyId,
        evaluation_result: result,
        redacted_context: safeContext
    };

    // In production, this vectors to CloudWatch / Datadog
    console.log(JSON.stringify(logEntry));
}
