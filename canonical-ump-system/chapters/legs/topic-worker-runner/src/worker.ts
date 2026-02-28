export interface TaskPayload {
    job_id: string;
    action: string;
}

const localMemoryQueue: TaskPayload[] = [];

export function startWorker(concurrency: number = 1): NodeJS.Timeout {
    console.log(`[LEGS WORKER] Worker daemon listening with concurrency ${concurrency}...`);

    return setInterval(() => {
        if (localMemoryQueue.length > 0) {
            const task = localMemoryQueue.shift();
            if (task) {
                console.log(`[LEGS WORKER] Picked up job ${task.job_id}: Executing Action [${task.action}]`);
            }
        }
    }, 100);
}

export function dispatchLocalTask(task: TaskPayload) {
    localMemoryQueue.push(task);
}

export function clearWorkspaceQueue() {
    localMemoryQueue.length = 0;
}
