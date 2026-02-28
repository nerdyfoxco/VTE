export interface CronJob {
    name: string;
    expression: string;
    handler: () => void;
}

const activeJobs: Record<string, NodeJS.Timeout> = {};

export function startCronManager() {
    console.log('[LEGS SCHEDULER] Booting Master Cron Manager System...');
}

export function registerJob(job: CronJob) {
    console.log(`[LEGS SCHEDULER] Registering Job [${job.name}] with expression "${job.expression}"`);

    const timer = setInterval(() => {
        console.log(`[LEGS SCHEDULER] Clock ticked for [${job.name}] -> Firing.`);
        job.handler();
    }, 100);

    activeJobs[job.name] = timer;
}

export function shutdownScheduler() {
    for (const name in activeJobs) {
        clearInterval(activeJobs[name]);
    }
}
