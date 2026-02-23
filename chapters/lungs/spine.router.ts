// Lungs Module: Spine Event Router & DLQ

export enum EventTopic {
    EXECUTION_SUCCESS = 'EXECUTION_SUCCESS',
    EXECUTION_FAILURE = 'EXECUTION_FAILURE',
    TENANT_VIOLATION = 'TENANT_VIOLATION'
}

export interface SpineEvent {
    topic: EventTopic;
    correlationId: string;
    workspaceId: string;
    timestamp: string;
    payload: any;
    errorContext?: string;
}

export class EventRouter {
    private deadLetterQueue: SpineEvent[] = [];
    private auditLogQueue: SpineEvent[] = [];

    public emit(event: SpineEvent): void {
        console.log(`[Lungs][EventRouter] Emitting [${event.topic}] for [${event.correlationId}]`);

        if (event.topic === EventTopic.EXECUTION_FAILURE || event.topic === EventTopic.TENANT_VIOLATION) {
            this.routeToDeadLetterQueue(event);
        } else {
            this.routeToAuditLog(event);
        }
    }

    private routeToDeadLetterQueue(event: SpineEvent): void {
        console.warn(`[Lungs][DLQ] Ingesting failed event [${event.correlationId}]. Reason: ${event.errorContext}`);
        this.deadLetterQueue.push(event);
        // In Prod: Publish to AWS SQS / Kafka DLQ topic for recovery analysis
    }

    private routeToAuditLog(event: SpineEvent): void {
        console.log(`[Lungs][Audit] Syncing event [${event.correlationId}] to compliance storage.`);
        this.auditLogQueue.push(event);
        // In Prod: Publish to immutable structured logging (e.g., Datadog, Splunk)
    }

    public getDeadLetterQueueSize(): number {
        return this.deadLetterQueue.length;
    }
}
