import { startServer } from './server';

const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3003;

startServer({ port })
    .then(({ port }) => {
        console.log(`Query API server listening on port ${port}`);
    })
    .catch((err) => {
        console.error('Failed to start Query API server:', err);
        process.exit(1);
    });
