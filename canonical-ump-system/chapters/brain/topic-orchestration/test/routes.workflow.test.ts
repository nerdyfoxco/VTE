import test from 'node:test';
import assert from 'node:assert';
import { startServer } from '../src/server';

test('POST /workflows/start Route', async (t) => {
    const server = await startServer({ port: 0 });
    const baseUrl = `http://localhost:${server.port}`;

    try {
        await t.test('Successfully starts a workflow and returns 201', async () => {
            const response = await fetch(`${baseUrl}/workflows/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    workflow_name: 'integration_test_wf',
                    initiator: 'Test Runner',
                    inputs: { test_key: 123 }
                })
            });

            assert.strictEqual(response.status, 201);
            const json = await response.json();
            assert.ok(json.workflow_id);
            assert.strictEqual(json.status, 'started');
            assert.ok(json.event_id);
        });

        await t.test('Rejects payload missing initiator field with 400', async () => {
            const response = await fetch(`${baseUrl}/workflows/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    workflow_name: 'bad_test',
                    inputs: {}
                })
            });

            assert.strictEqual(response.status, 400);
            const json = await response.json();
            assert.strictEqual(json.error, 'Missing required fields: workflow_name, initiator, inputs');
        });

    } finally {
        await server.close();
    }
});
