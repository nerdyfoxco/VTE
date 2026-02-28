import test from 'node:test';
import assert from 'node:assert';
import { executeWithSafety } from '../../src/engine/shadow-wrapper';

test('Shadow Engine Wrapper Strict Logic', async (t) => {
    let wasAdapterCalled = false;

    const mockAdapter = () => {
        wasAdapterCalled = true;
        return { receipt_id: 'adapter_live_execution_123' };
    };

    t.beforeEach(() => {
        wasAdapterCalled = false;
    });

    await t.test('Defaults to Shadow execution when token is explicitly "dry-run"', () => {
        const payload = {
            data: {
                action: 'send_email',
                target_system: 'gmail',
                parameters: { to: 'test@example.com' },
                execution_authz: {
                    token: 'dry-run',
                    approved_by: 'system',
                    risk_tier: 1
                }
            }
        };

        const receipt = executeWithSafety(payload, mockAdapter);

        assert.strictEqual(receipt.status, 'shadow');
        assert.strictEqual(wasAdapterCalled, false);
        assert.ok(receipt.receipt_id.startsWith('shadow_'));
    });

    await t.test('Defaults to Shadow execution when risk_tier is dangerously high', () => {
        const payload = {
            data: {
                action: 'evict_tenant',
                target_system: 'appfolio',
                parameters: { tenant_id: 'danger_1' },
                execution_authz: {
                    token: 'genuine_crypto_token',
                    approved_by: 'admin',
                    risk_tier: 5  // Abnormally high risk!
                }
            }
        };

        const receipt = executeWithSafety(payload, mockAdapter);

        assert.strictEqual(receipt.status, 'shadow');
        assert.strictEqual(wasAdapterCalled, false);
    });

    await t.test('Executes physical live adapter when token is genuine and risk is low', () => {
        const payload = {
            data: {
                action: 'send_email',
                target_system: 'gmail',
                parameters: { to: 'real_tenant@example.com' },
                execution_authz: {
                    token: 'genuine_crypto_token',
                    approved_by: 'pm_manager',
                    risk_tier: 1
                }
            }
        };

        const receipt = executeWithSafety(payload, mockAdapter);

        assert.strictEqual(receipt.status, 'live');
        assert.strictEqual(wasAdapterCalled, true);
        assert.strictEqual(receipt.receipt_id, 'adapter_live_execution_123');
    });
});
