import test from 'node:test';
import assert from 'node:assert';
import { startServer } from '../src/server';

test('Query API Smoke Test', async (t) => {
    let serverInstance: { port: number, close: () => Promise<void> };

    t.before(async () => {
        serverInstance = await startServer({ port: 0 }); // Pick any available port
    });

    t.after(async () => {
        if (serverInstance) {
            await serverInstance.close();
        }
    });

    await t.test('GET /healthz returns 200 ok and service identifier', async () => {
        const url = `http://localhost:${serverInstance.port}/healthz`;
        const res = await fetch(url);
        assert.strictEqual(res.status, 200);

        const body = await res.json();
        assert.deepStrictEqual(body, { status: 'ok', service: 'query-api' });
    });

    await t.test('GET /unknown returns 404', async () => {
        const url = `http://localhost:${serverInstance.port}/unknown`;
        const res = await fetch(url);
        assert.strictEqual(res.status, 404);
    });
});
