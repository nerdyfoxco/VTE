import test from 'node:test';
import assert from 'node:assert';
import { evaluatePolicy } from '../../src/rules/evaluator';

test('evaluatePolicy (Canonical Pure Functions)', async (t) => {
    await t.test('passes eviction_threshold_v1 correctly', () => {
        const result = evaluatePolicy('policy_eviction_threshold_v1', { months_delinquent: 3 });
        assert.strictEqual(result.passed, true);
    });

    await t.test('fails eviction_threshold_v1 correctly', () => {
        const result = evaluatePolicy('policy_eviction_threshold_v1', { months_delinquent: 1 });
        assert.strictEqual(result.passed, false);
    });

    await t.test('passes spending_limit_v1 correctly', () => {
        const result = evaluatePolicy('policy_spending_limit_v1', { amount_usd: 500 });
        assert.strictEqual(result.passed, true);
    });

    await t.test('throws ERR_POLICY_NOT_FOUND on invalid policy', () => {
        assert.throws(
            () => evaluatePolicy('invalid_id', {}),
            (err: any) => err.code === 'ERR_POLICY_NOT_FOUND' && err.message.includes('Unknown policy ID')
        );
    });
});
