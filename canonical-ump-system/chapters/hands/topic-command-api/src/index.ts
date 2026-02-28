import { startServer } from './server';

const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3002;

startServer({ port })
    .then(({ port }) => {
        console.log(`Command API server listening on port ${port}`);
    })
    .catch((err) => {
        console.error('Failed to start Command API server:', err);
        process.exit(1);
    });
