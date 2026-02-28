import test from 'node:test';
import assert from 'node:assert';
import { handlePolicyEvaluatePipe } from '../../src/pipes/evaluate-consumer';
import { ContractRunner } from '../../../../../foundation/src/testing/contract-runner';

test('Integration: Policy Engine Pipeline (topic-orchestration ↔ topic-policy-engine)', async (t) => {
    const runner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.policy.evaluated.v1.schema.json');

    await t.test('consumes valid evaluate request and returns compliant evaluated success response', () => {
        // 1. Mock the request from topic-orchestration
        const requestPayload = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174010',
                producer: 'chapters/brain/topic-orchestration',
                schema_version: '1.0.0'
            },
            data: {
                policy_id: 'policy_eviction_threshold_v1',
                context: {
                    tenant_ssn: '123-456-7890',
                    months_delinquent: 5
                },
                requester: 'test-runner',
                dry_run: false
            }
        };

        // 2. Consume & Evaluate
        const responsePayload = handlePolicyEvaluatePipe(requestPayload);

        // 3. Assert Outbound Canonical Schema Compliance
        runner.assertValid(responsePayload);

        // 4. Assert Business Logic Determinism
        const payloadData = (responsePayload as any).data;
        const payloadMeta = (responsePayload as any).meta;

        assert.strictEqual(payloadData.passed, true);
        assert.strictEqual(payloadData.policy_id, 'policy_eviction_threshold_v1');
        assert.strictEqual(payloadData.original_event_id, requestPayload.meta.event_id);
        assert.strictEqual(payloadMeta.correlation_id, '123e4567-e89b-12d3-a456-426614174010');
    });

    await t.test('consumes evaluate request and explicitly returns failed outcome contextually', () => {
        const requestPayload = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174010',
                producer: 'chapters/brain/topic-orchestration',
                schema_version: '1.0.0'
            },
            data: {
                policy_id: 'policy_eviction_threshold_v1',
                context: {
                    months_delinquent: 0
                },
                requester: 'test-runner',
                dry_run: false
            }
        };

        const responsePayload = handlePolicyEvaluatePipe(requestPayload);
        runner.assertValid(responsePayload);

        const payloadData = (responsePayload as any).data;
        assert.strictEqual(payloadData.passed, false);
    });
});
