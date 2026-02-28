import * as http from 'http';
import { AddressInfo } from 'net';
import { WorkflowStore } from './workflow-store';
import { handleWorkflowRoutes } from './routes/workflow.routes';

export function startServer({ port }: { port: number }): Promise<{ port: number, close(): Promise<void> }> {
    // Initialize in-memory singleton for the orchestration node boundaries
    const workflowStore = new WorkflowStore();

    return new Promise((resolve) => {
        const server = http.createServer((req, res) => {
            // Primary HTTP routing
            if (req.method === 'GET' && req.url === '/healthz') {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'ok' }));
                return;
            }

            const routeHandled = handleWorkflowRoutes(workflowStore, req, res);
            if (routeHandled) return;

            // Fallback
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'not_found' }));
        });

        server.listen(port, () => {
            const address = server.address() as AddressInfo;
            resolve({
                port: address.port,
                close: () => new Promise<void>((resClose, rejClose) => {
                    server.close((err) => {
                        if (err) return rejClose(err);
                        resClose();
                    });
                }),
            });
        });
    });
} 
