import * as http from 'http';
import { randomUUID } from 'crypto';
import { emitWorkflowStarted, WorkflowStartedData } from '../pipes/workflow-started.producer';
import { WorkflowStore } from '../workflow-store';

export function handleWorkflowRoutes(store: WorkflowStore, req: http.IncomingMessage, res: http.ServerResponse): boolean {
    if (req.method === 'POST' && req.url === '/workflows/start') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            try {
                const payload: Partial<WorkflowStartedData> = JSON.parse(body);

                if (!payload.workflow_name || !payload.initiator || !payload.inputs) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'Missing required fields: workflow_name, initiator, inputs' }));
                    return;
                }

                const workflowId = randomUUID();

                // 1. Idempotent State Mutation
                try {
                    store.createWorkflow(workflowId, payload.workflow_name);
                } catch (err: any) {
                    if (err.code === 'ERR_WORKFLOW_EXISTS') {
                        res.writeHead(409, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ error: err.message }));
                        return;
                    }
                    throw err;
                }

                // 2. Strict AJV Validated Pipe Emission
                const startedData: WorkflowStartedData = {
                    workflow_id: workflowId,
                    workflow_name: payload.workflow_name,
                    initiator: payload.initiator,
                    inputs: payload.inputs
                };

                const emitted = emitWorkflowStarted(startedData);

                res.writeHead(201, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    workflow_id: workflowId,
                    status: 'started',
                    event_id: emitted.meta.event_id
                }));

            } catch (err: any) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: err.message || 'Internal Server Error' }));
            }
        });

        return true; // Handled
    }

    return false; // Not handled
}
