import test from 'node:test';
import assert from 'node:assert';
import { WorkflowStore } from '../src/workflow-store';

test('Workflow Store Idempotency & State', async (t) => {
    const store = new WorkflowStore();
    const wfId = 'wf-123-abc';

    await t.test('creates a new workflow successfully', () => {
        const wf = store.createWorkflow(wfId, 'Eviction_Process');
        assert.strictEqual(wf.workflow_id, wfId);
        assert.strictEqual(wf.status, 'started');
        assert.strictEqual(wf.workflow_name, 'Eviction_Process');
    });

    await t.test('enforces idempotency by rejecting duplicate workflow_id', () => {
        assert.throws(() => {
            store.createWorkflow(wfId, 'Eviction_Process_Duplicate');
        }, (err: any) => err.code === 'ERR_WORKFLOW_EXISTS');
    });

    await t.test('retrieves existing workflow', () => {
        const wf = store.getWorkflow(wfId);
        assert.ok(wf);
        assert.strictEqual(wf.status, 'started');
    });

    await t.test('completes step', () => {
        const updated = store.completeStep(wfId, 'step-01');
        assert.strictEqual(updated.status, 'completed');
    });

    await t.test('throws on unknown workflow completion', () => {
        assert.throws(() => {
            store.completeStep('unknown-wf', 'step-01');
        }, (err: any) => err.code === 'ERR_WORKFLOW_NOT_FOUND');
    });
});
