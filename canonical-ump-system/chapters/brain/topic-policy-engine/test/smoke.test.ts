import test from 'node:test';
import assert from 'node:assert';
import { startServer } from '../src/server';

test('Policy Engine Smoke Test', async (t) => {
    const server = await startServer({ port: 0 }); // ephemeral port
    const baseUrl = `http://localhost:${server.port}`;

    try {
        await t.test('GET /healthz returns 200 ok and service identifier', async () => {
            const response = await fetch(`${baseUrl}/healthz`);
            assert.strictEqual(response.status, 200);

            const json = await response.json();
            assert.strictEqual(json.status, 'ok');
            assert.strictEqual(json.service, 'policy-engine');
        });

        await t.test('GET /unknown returns 404', async () => {
            const response = await fetch(`${baseUrl}/unknown`);
            assert.strictEqual(response.status, 404);
        });

    } finally {
        await server.close();
    }
});
