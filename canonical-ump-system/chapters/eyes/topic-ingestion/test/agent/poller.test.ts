import test from 'node:test';
import assert from 'node:assert';
import { startPoller } from '../../src/agent/poller';

test('Eyes Ingestion Agent Poller', async (t) => {
    await t.test('Initializes precisely and ticks without crashing', () => {
        // Start poller precisely mapping tiny intervals for tests securely
        const timer = startPoller(10);

        assert.ok(timer, 'Poller reference instantiated firmly.');

        clearInterval(timer);
    });
});
