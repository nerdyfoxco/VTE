export function pollAppFolio() {
    console.log('[POLLER] Fetching evidence from AppFolio...');
}

export function pollGmail() {
    console.log('[POLLER] Fetching evidence from Gmail...');
}

export function startPoller(intervalMs: number = 60000): NodeJS.Timeout {
    console.log(`[POLLER] Starting Ingestion Agent Poller (Interval: ${intervalMs}ms)`);

    return setInterval(() => {
        console.log('[POLLER] Polling event loop ticked...');
        pollAppFolio();
        pollGmail();
    }, intervalMs);
}
