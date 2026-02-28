import test from 'node:test';
import assert from 'node:assert';
import { CircuitController } from '../../src/circuit/breaker';

test('Hands Circuit Controller Engine', async (t) => {
    await t.test('allows executions under the threshold', () => {
        const breaker = new CircuitController();

        for (let i = 0; i < 9; i++) {
            assert.strictEqual(breaker.checkExecutionTolerance('mockSystem'), true);
        }
    });

    await t.test('trips the circuit strictly on the 11th request', () => {
        const breaker = new CircuitController();

        // Push 10 identical executions gracefully
        for (let i = 0; i < 10; i++) {
            assert.strictEqual(breaker.checkExecutionTolerance('mockSystem_Trip_Test'), true);
        }

        // Attempt 11 immediately throws ERR_CIRCUIT_TRIPPED
        assert.throws(
            () => breaker.checkExecutionTolerance('mockSystem_Trip_Test'),
            (err: any) => err.code === 'ERR_CIRCUIT_TRIPPED' && err.message.includes('exceeded max mutations')
        );
    });

    await t.test('isolates target systems tracking independently', () => {
        const breaker = new CircuitController();

        for (let i = 0; i < 10; i++) {
            assert.strictEqual(breaker.checkExecutionTolerance('target_A'), true);
        }

        assert.strictEqual(breaker.checkExecutionTolerance('target_B'), true);
    });
});
