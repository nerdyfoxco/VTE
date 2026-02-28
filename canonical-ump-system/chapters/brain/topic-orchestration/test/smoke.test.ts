import test from 'node:test';
import assert from 'node:assert';
import { startServer } from '../src/server';

test('GET /healthz returns 200 ok', async (t) => {
    const server = await startServer({ port: 0 });
    try {
        const res = await fetch(`http://localhost:${server.port}/healthz`);
        assert.strictEqual(res.status, 200);
        const body = await res.json();
        assert.deepStrictEqual(body, { status: 'ok' });
    } finally {
        await server.close();
    }
});
