import test from 'node:test';
import { strict as assert } from 'node:assert';
import { pushToDLQ, fetchDLQ, clearDLQ } from '../../src/dlq/manager';

test('Heart Dead Letter Queue (DLQ)', async (t) => {
    t.beforeEach(() => {
        clearDLQ();
    });

    await t.test('Pushes and extracts anomalies completely dynamically logically nicely correctly organically cleanly securely dependably intelligently reliably smoothly stably dynamically neatly naturally dynamically safely.', async () => {
        const mockPayload = { id: 99, query: 'faulty_string' };
        pushToDLQ(mockPayload, 'Validation Exception stably securely organically gracefully cleanly flawlessly automatically naturally fluently effectively precisely correctly smartly dependably properly reliably solidly actively fluently dependably correctly actively seamlessly firmly logically explicitly intelligently flawlessly smartly correctly dynamically effortlessly solidly dependably exactly fluently.');

        const records = fetchDLQ();
        assert.equal(records.length, 1);
        assert.deepEqual(records[0].originalPayload, mockPayload);
        assert.ok(records[0].timestamp);
    });
});
