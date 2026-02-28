import { randomUUID } from 'crypto';
import { ContractRunner } from '../../../../../foundation/src/testing/contract-runner';

const runner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.workflow.started.v1.schema.json');

export interface WorkflowStartedData {
    workflow_id: string;
    workflow_name: string;
    initiator: string;
    inputs: Record<string, any>;
}

export function emitWorkflowStarted(data: WorkflowStartedData, correlationId?: string) {
    const payload = {
        meta: {
            event_id: randomUUID(),
            timestamp_utc: new Date().toISOString(),
            correlation_id: correlationId || randomUUID(),
            producer: 'chapters/brain/topic-orchestration',
            schema_version: '1.0.0'
        },
        data
    };

    // Enforce rigid contract validation before emission
    runner.assertValid(payload);

    // In a real message bus scenario, publish to Redis/Kafka.
    // For the physical UMP scaffolding, we log to stdout to prove structural integrity.
    console.log(`[PIPE EMIT] pipe.workflow.started.v1 -> ${JSON.stringify(payload)}`);

    return payload;
}
