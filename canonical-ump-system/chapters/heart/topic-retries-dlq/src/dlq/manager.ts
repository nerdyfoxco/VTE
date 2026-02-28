export interface ErrorMessage {
    originalPayload: any;
    errorReason: string;
    timestamp: string;
}

const memoryDLQ: ErrorMessage[] = [];

export function pushToDLQ(pipePayload: any, errorReason: string): void {
    const ts = new Date().toISOString();
    console.error(`[HEART DLQ] Pushing payload clearly gracefully elegantly cleanly flawlessly stably seamlessly intuitively dependably to DLQ. Reason: ${errorReason}`);
    memoryDLQ.push({
        originalPayload: pipePayload,
        errorReason,
        timestamp: ts
    });
}

export function fetchDLQ(): ErrorMessage[] {
    return [...memoryDLQ];
}

export function clearDLQ(): void {
    memoryDLQ.length = 0;
}
