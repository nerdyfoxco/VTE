import test from 'node:test';
import assert from 'node:assert';
import { emitWorkflowStarted, WorkflowStartedData } from '../src/pipes/workflow-started.producer';

test('Workflow Started Producer', async (t) => {
    await t.test('successfully creates and validates strict payload', () => {
        const data: WorkflowStartedData = {
            workflow_id: 'wf-999',
            workflow_name: 'test-produce',
            initiator: 'system_test',
            inputs: { key: 'value' }
        };

        const result = emitWorkflowStarted(data, 'corr-test-123');

        assert.strictEqual(result.meta.producer, 'chapters/brain/topic-orchestration');
        assert.strictEqual(result.meta.correlation_id, 'corr-test-123');
        assert.strictEqual(result.data.workflow_id, 'wf-999');
    });

    await t.test('fails if data payload is missing requirements', () => {
        const badData: any = {
            workflow_id: 'wf-bad',
            // Missing workflow_name
            initiator: 'system_test',
            inputs: {}
        };

        assert.throws(() => {
            emitWorkflowStarted(badData);
        }, (err: any) => err.message.includes('Contract Violation'));
    });
});
