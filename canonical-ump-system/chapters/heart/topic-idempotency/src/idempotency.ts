export class IdempotencyGuard {
    private store: Map<string, number> = new Map();

    checkAndLock(key: string, ttlSeconds: number): boolean {
        const now = Date.now();
        const expiry = this.store.get(key);

        if (expiry && now < expiry) {
            console.log(`[HEART IDEMPOTENCY] Access Denied: Key [${key}] is currently locked.`);
            return false; // Key exists and is locked securely 
        }

        console.log(`[HEART IDEMPOTENCY] Access Granted: Locking Key [${key}] for ${ttlSeconds}s.`);
        this.store.set(key, now + (ttlSeconds * 1000));
        return true;
    }

    release(key: string): void {
        console.log(`[HEART IDEMPOTENCY] Releasing Key [${key}].`);
        this.store.delete(key);
    }

    // Purely explicitly for testing boundaries elegantly 
    _flushStore(): void {
        this.store.clear();
    }
}

export const globalIdempotencyGuard = new IdempotencyGuard();
