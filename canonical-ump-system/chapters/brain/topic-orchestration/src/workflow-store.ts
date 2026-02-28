export interface WorkflowState {
    workflow_id: string;
    workflow_name: string;
    status: 'started' | 'completed';
    created_at_utc: string;
}

export class WorkflowStore {
    private store: Map<string, WorkflowState> = new Map();

    public createWorkflow(workflowId: string, workflowName: string): WorkflowState {
        if (this.store.has(workflowId)) {
            const err: any = new Error(`Workflow ${workflowId} already exists.`);
            err.code = 'ERR_WORKFLOW_EXISTS';
            throw err;
        }

        const state: WorkflowState = {
            workflow_id: workflowId,
            workflow_name: workflowName,
            status: 'started',
            created_at_utc: new Date().toISOString()
        };

        this.store.set(workflowId, state);
        return state;
    }

    public getWorkflow(workflowId: string): WorkflowState | undefined {
        return this.store.get(workflowId);
    }

    public completeStep(workflowId: string, _stepId: string): WorkflowState {
        const state = this.store.get(workflowId);
        if (!state) {
            const err: any = new Error(`Workflow ${workflowId} not found.`);
            err.code = 'ERR_WORKFLOW_NOT_FOUND';
            throw err;
        }

        // simplistic placeholder for now: marking workflow as completed
        state.status = 'completed';
        this.store.set(workflowId, state);

        return state;
    }
}
