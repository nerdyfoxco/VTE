import test from 'node:test';
import assert from 'node:assert';
import { ContractRunner } from '../../../../foundation/src/testing/contract-runner';

test('Contract: pipe.policy.evaluate.v1', async (t) => {
    const runner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.policy.evaluate.v1.schema.json');

    await t.test('Validates a compliant payload', () => {
        const validPayload = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174001',
                producer: 'test-runner',
                schema_version: '1.0.0'
            },
            data: {
                policy_id: 'eviction_grace_period',
                context: {
                    tenant_arrears: 1500,
                    filing_date: '2026-02-01'
                },
                requester: 'system',
                dry_run: false
            }
        };

        runner.assertValid(validPayload);
        console.log('CONTRACT_OK pipe.policy.evaluate.v1');
    });

    await t.test('Rejects payload with missing requester', () => {
        const invalidPayload = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174002',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174001',
                producer: 'test-runner',
                schema_version: '1.0.0'
            },
            data: {
                policy_id: 'eviction_grace_period',
                context: {},
                dry_run: false
            }
        };

        runner.assertInvalid(invalidPayload);
    });
});
