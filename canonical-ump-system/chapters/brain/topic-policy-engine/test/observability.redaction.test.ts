import test from 'node:test';
import assert from 'node:assert';
import { redactContext } from '../../../../foundation/src/security/redact';

test('Security Redaction Logic', async (t) => {
    await t.test('strips SSN and passwords but preserves standard metrics', () => {
        const maliciousPayload = {
            user_id: 'tenant_uuid',
            ssn: '123-45',
            months_delinquent: 2,
            nested_data: {
                password: 'secure_password'
            }
        };

        const safePayload = redactContext(maliciousPayload);

        assert.strictEqual(safePayload.user_id, 'tenant_uuid');
        assert.strictEqual(safePayload.months_delinquent, 2);
        assert.strictEqual(safePayload.ssn, '[REDACTED]');
        assert.strictEqual(safePayload.nested_data.password, '[REDACTED]');
    });
});
