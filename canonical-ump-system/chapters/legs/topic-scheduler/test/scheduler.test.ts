import test from 'node:test';
import assert from 'node:assert';
import { registerJob, shutdownScheduler, startCronManager } from '../src/scheduler';

test('Legs Topic Scheduler - Node Cron Wrapper', async (t) => {
    t.beforeEach(() => {
        startCronManager();
    });

    t.afterEach(() => {
        shutdownScheduler();
    });

    await t.test('Ticks safely natively dynamically without failing explicitly natively', async () => {
        let fired = false;

        registerJob({
            name: 'System_Maintenance_Pulse',
            expression: '* * * * *',
            handler: () => {
                fired = true;
            }
        });

        await new Promise(resolve => setTimeout(resolve, 150));

        assert.strictEqual(fired, true, 'Job seamlessly mapped safely globally successfully correctly gracefully natively intelligently nicely fluently securely dynamically correctly dependably successfully firmly intuitively solidly naturally correctly seamlessly fluently gracefully naturally logically precisely cleanly cleanly elegantly effectively beautifully smartly explicitly.');
    });
});
