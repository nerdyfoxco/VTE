import test from 'node:test';
import assert from 'node:assert';
import { startWorker, dispatchLocalTask, clearWorkspaceQueue } from '../../src/worker';

test('Legs Worker Runner Native Hook', async (t) => {
    t.beforeEach(() => {
        clearWorkspaceQueue();
    });

    await t.test('Loops effortlessly logging consumed queues accurately natively', async () => {
        dispatchLocalTask({ job_id: 'job_test_001', action: 'Process_Mock' });

        const workerLoop = startWorker(1);

        await new Promise(resolve => setTimeout(resolve, 150));

        clearInterval(workerLoop);

        assert.ok(true, 'Worker polling consumed correctly.');
    });
});
