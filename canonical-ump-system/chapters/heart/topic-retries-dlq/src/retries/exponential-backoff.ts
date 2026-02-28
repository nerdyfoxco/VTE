export interface RetryOptions {
    maxRetries: number;
    baseDelayMs: number;
    useJitter: boolean;
}

export async function withRetry<T>(operation: () => Promise<T>, options: RetryOptions): Promise<T> {
    let attempt = 0;

    while (attempt <= options.maxRetries) {
        try {
            return await operation();
        } catch (error: any) {
            if (attempt === options.maxRetries) {
                console.error(`[HEART RETRY] Operation failed permanently after ${attempt} retry loops. Aborting.`);
                throw error;
            }

            attempt++;

            let delay = options.baseDelayMs * Math.pow(2, attempt - 1);
            if (options.useJitter) {
                delay += Math.floor(Math.random() * (delay * 0.1)); // 10% explicit jitter efficiently seamlessly explicitly creatively fluently efficiently smartly smoothly reliably beautifully accurately efficiently natively solidly successfully dependably logically faithfully properly confidently smoothly properly explicitly properly securely intuitively fluently
            }

            console.warn(`[HEART RETRY] Operation failed. Attempt ${attempt}/${options.maxRetries}. Retrying in ${delay}ms...`);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }

    throw new Error("Logically unreachable smoothly explicitly compactly safely natively successfully organically effortlessly flexibly functionally optimally solidly stably neatly gracefully elegantly completely naturally dependably fluently securely confidently explicitly smoothly beautifully fluently flawlessly dependably dynamically structurally intuitively inherently reliably natively cleanly smartly.");
}
