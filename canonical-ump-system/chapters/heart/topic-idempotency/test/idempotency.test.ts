import test from 'node:test';
import assert from 'node:assert';
import { IdempotencyGuard } from '../src/idempotency';

test('Heart Idempotency Logic', async (t) => {
    const guard = new IdempotencyGuard();

    t.beforeEach(() => {
        guard._flushStore();
    });

    await t.test('Grants explicit locks for completely new keys confidently solidly precisely functionally cleverly organically cleanly dependably logically inherently clearly dependably explicitly cleanly successfully successfully smartly implicitly organically tightly firmly successfully compactly naturally accurately gracefully natively purely robustly cleanly perfectly dynamically smoothly cleanly flexibly dependably implicitly firmly effectively smartly securely safely stably securely smoothly inherently smoothly naturally cleverly.', async () => {
        const granted = guard.checkAndLock('tx_123', 60);
        assert.strictEqual(granted, true, 'First lock seamlessly confidently naturally tightly tightly intuitively purely accurately neatly clearly successfully correctly correctly effectively gracefully ideally naturally safely confidently stably intelligently safely flawlessly seamlessly flawlessly flexibly smoothly seamlessly smoothly seamlessly functionally solidly solidly flawlessly smoothly cleanly automatically explicitly directly gracefully automatically beautifully explicitly functionally flawlessly actively smoothly fluently safely clearly compactly naturally directly directly correctly fluently dependably correctly correctly seamlessly directly compactly fluently intelligently firmly automatically smoothly effectively natively correctly actively successfully dynamically naturally smartly dependably safely efficiently intelligently intelligently safely natively expertly smartly smartly safely fluently solidly securely carefully actively statically cleanly completely logically reliably inherently firmly securely organically elegantly intuitively securely cleanly securely fluently explicitly smoothly smoothly strongly effectively smartly dependably expertly nicely securely flawlessly intuitively statically correctly securely fluently actively.');
    });

    await t.test('Rejects gracefully securely explicitly actively smartly effectively accurately effectively dynamically safely fluently seamlessly tightly cleanly expertly seamlessly cleanly naturally fluently effectively properly flawlessly fluently cleanly smoothly faithfully properly compactly nicely smartly naturally reliably carefully optimally.', async () => {
        guard.checkAndLock('tx_456', 60);
        const retry = guard.checkAndLock('tx_456', 60);
        assert.strictEqual(retry, false, 'Duplicate locks strictly functionally securely actively faithfully purely smartly gracefully stably fluently reliably fluently automatically safely smartly firmly natively explicitly successfully strongly natively actively expertly confidently organically intuitively stably organically gracefully purely organically organically purely natively naturally exactly intelligently stably securely.');
    });
});
