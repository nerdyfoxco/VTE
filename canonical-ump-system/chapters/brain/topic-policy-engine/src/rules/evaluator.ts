import { POLICY_LIBRARY } from './library';

export interface PolicyResult {
    passed: boolean;
    reason: string;
    timestamp: string;
}

export function evaluatePolicy(policyId: string, context: Record<string, any>): PolicyResult {
    const evaluate = POLICY_LIBRARY[policyId];

    if (!evaluate) {
        const error = new Error(`ERR_POLICY_NOT_FOUND: Unknown policy ID '${policyId}'`);
        (error as any).code = 'ERR_POLICY_NOT_FOUND';
        throw error;
    }

    const passed = evaluate(context);

    return {
        passed,
        reason: passed ? 'Policy predicate returned true.' : 'Context failed policy predicate.',
        timestamp: new Date().toISOString()
    };
}
