export interface ComputedEffect {
    target: string;
    action: string;
    payloadDrop: any;
}
export interface WorkflowRequest {
    workflowName: string;
    payload: any;
}
export interface ShadowExecutionResult {
    traceId: string;
    mode: 'SHADOW' | 'LIVE';
    status: 'SIMULATED_SUCCESS' | 'EXECUTED_SUCCESS' | 'HALTED';
    simulatedEffects: any[];
}
export declare class ShadowExecutionEngine {
    private prisma;
    private dispatcher;
    constructor();
    /**
     * Replicates the exact logical pathway of a requested Workflow without firing side-effects.
     * Records an explicit SHADOW trace to the Canonical Database.
     */
    routeInShadowMode(tenantId: string, operatorId: string, request: WorkflowRequest): Promise<ShadowExecutionResult>;
    /**
     * Replicates the exact logical pathway of `routeInShadowMode`, but explicitly
     * hands the projected effects off to the Hands module via the Dispatcher.
     * Records a LIVE_EXECUTED trace in the Canonical Database.
     */
    routeInLiveMode(tenantId: string, operatorId: string, request: WorkflowRequest): Promise<ShadowExecutionResult>;
    /**
     * Pure function determining projected Side-Effects (e.g., SendGrid emails, AppFolio DB inserts)
     * based entirely on the shape of the Kidney-validated payload.
     */
    private computeSideEffects;
}
