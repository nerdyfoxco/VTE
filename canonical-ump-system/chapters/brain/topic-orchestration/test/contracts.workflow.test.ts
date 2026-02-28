import test from 'node:test';
import assert from 'node:assert';
import { ContractRunner } from '../../../../foundation/src/testing/contract-runner';

test('Workflow Started Pipe Contract Validations', async (t) => {
    const runner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.workflow.started.v1.schema.json');

    await t.test('accepts valid payload', () => {
        const validPayload = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: '2026-02-25T12:00:00Z',
                correlation_id: 'corr-123',
                producer: 'brain/topic-orchestration',
                schema_version: '1.0.0'
            },
            data: {
                workflow_id: 'wf-123',
                workflow_name: 'test_workflow',
                initiator: 'system',
                inputs: { someParam: "value" }
            }
        };
        runner.assertValid(validPayload);
    });

    await t.test('rejects payload missing required meta', () => {
        const invalidPayload = {
            data: {
                workflow_id: 'wf-123',
                workflow_name: 'test_workflow',
                initiator: 'system',
                inputs: {}
            }
        };
        runner.assertInvalid(invalidPayload);
    });
});

test('Workflow Step Completed Pipe Contract Validations', async (t) => {
    const runner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.workflow.step.completed.v1.schema.json');

    await t.test('accepts valid success payload', () => {
        const validPayload = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174001',
                timestamp_utc: '2026-02-25T12:05:00Z',
                correlation_id: 'corr-123',
                producer: 'hands/worker-node',
                schema_version: '1.0.0'
            },
            data: {
                workflow_id: 'wf-123',
                step_id: 'step-1',
                step_name: 'charge_fee',
                status: 'success',
                outputs: { receipt: "ok" }
            }
        };
        runner.assertValid(validPayload);
    });

    await t.test('rejects invalid status enum', () => {
        const invalidPayload = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174001',
                timestamp_utc: '2026-02-25T12:05:00Z',
                correlation_id: 'corr-123',
                producer: 'hands/worker-node',
                schema_version: '1.0.0'
            },
            data: {
                workflow_id: 'wf-123',
                step_id: 'step-1',
                step_name: 'charge_fee',
                status: 'PENDING_INVALID', // Enum violation
                outputs: {}
            }
        };
        runner.assertInvalid(invalidPayload);
    });
});
