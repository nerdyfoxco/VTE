export enum WorkItemState {
    INIT = 'INIT',
    IDENTITY_CHECK = 'IDENTITY_CHECK',
    LEDGER_PARSE = 'LEDGER_PARSE',
    ELIGIBILITY = 'ELIGIBILITY',
    DECISION = 'DECISION',
    HOLD = 'HOLD',
    STOP = 'STOP',
    APPROVED = 'APPROVED',
    MESSAGE_PREVIEW = 'MESSAGE_PREVIEW',
    EXECUTION = 'EXECUTION',
    COMPLETE = 'COMPLETE'
}

type EventPayload = any;

interface TransitionRule {
    from: WorkItemState;
    to: WorkItemState[];
}

// The immutable state lifecycle per VTE 3.0 specs
const ALLOWED_TRANSITIONS: TransitionRule[] = [
    { from: WorkItemState.INIT, to: [WorkItemState.IDENTITY_CHECK, WorkItemState.STOP] },
    { from: WorkItemState.IDENTITY_CHECK, to: [WorkItemState.LEDGER_PARSE, WorkItemState.STOP] },
    { from: WorkItemState.LEDGER_PARSE, to: [WorkItemState.ELIGIBILITY, WorkItemState.HOLD, WorkItemState.STOP] },
    { from: WorkItemState.ELIGIBILITY, to: [WorkItemState.DECISION, WorkItemState.HOLD, WorkItemState.STOP] },
    { from: WorkItemState.DECISION, to: [WorkItemState.APPROVED, WorkItemState.HOLD, WorkItemState.STOP] },
    { from: WorkItemState.HOLD, to: [WorkItemState.APPROVED, WorkItemState.STOP] }, // Requires Supervisor Override
    { from: WorkItemState.STOP, to: [] }, // Terminal State. No escape.
    { from: WorkItemState.APPROVED, to: [WorkItemState.MESSAGE_PREVIEW] },
    { from: WorkItemState.MESSAGE_PREVIEW, to: [WorkItemState.EXECUTION, WorkItemState.HOLD] },
    { from: WorkItemState.EXECUTION, to: [WorkItemState.COMPLETE, WorkItemState.HOLD] } // HOLD on retry limit hit
];

export class WorkflowEngine {
    constructor() { }

    /**
     * Deterministic, fail-closed state transition.
     */
    public transition(currentState: WorkItemState, targetState: WorkItemState, eventPayload: EventPayload): WorkItemState {
        const rule = ALLOWED_TRANSITIONS.find(t => t.from === currentState);

        if (!rule) {
            throw new Error(`[BrainEngine] FATAL: Unmapped state encountered: ${currentState}`);
        }

        if (!rule.to.includes(targetState)) {
            throw new Error(`[BrainEngine] CRITICAL SECURITY FAULT: Illegal state transition attempted from [${currentState}] to [${targetState}]. Execution aborted.`);
        }

        // Return the validated next state. Payload mutation occurs centrally in the Orchestrator loop.
        return targetState;
    }
}
