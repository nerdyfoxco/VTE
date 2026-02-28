import * as http from 'http';
import { AddressInfo } from 'net';

export function startServer({ port }: { port: number }): Promise<{ port: number, close(): Promise<void> }> {
    return new Promise((resolve) => {
        const server = http.createServer((req, res) => {
            if (req.method === 'GET' && req.url === '/healthz') {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'ok', service: 'command-api' }));
                return;
            }

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
