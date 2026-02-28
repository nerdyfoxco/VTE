export class CircuitController {
    private executionLog: Map<string, number[]> = new Map();
    private readonly MAX_EXECUTIONS_PER_MINUTE = 10;
    private readonly WINDOW_MS = 60000;

    public checkExecutionTolerance(targetSystem: string): boolean {
        const now = Date.now();
        let timestamps = this.executionLog.get(targetSystem) || [];

        // Filter out timestamps older than the sliding window
        timestamps = timestamps.filter(ts => (now - ts) < this.WINDOW_MS);

        if (timestamps.length >= this.MAX_EXECUTIONS_PER_MINUTE) {
            console.error(`[CIRCUIT BREAKER] Tripped for ${targetSystem}! Execution threshold exceeded.`);

            const error = new Error(`ERR_CIRCUIT_TRIPPED: Target system '${targetSystem}' exceeded max mutations per minute.`);
            (error as any).code = 'ERR_CIRCUIT_TRIPPED';
            throw error;
        }

        // Record the explicit execution
        timestamps.push(now);
        this.executionLog.set(targetSystem, timestamps);

        return true; // Circuit CLOSED (Safe)
    }

    // Debug functionality allowing resets natively
    public clearCircuits() {
        this.executionLog.clear();
    }
}

export const globalCircuitController = new CircuitController();
