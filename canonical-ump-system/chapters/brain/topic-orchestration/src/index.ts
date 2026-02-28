import { startServer } from './server';

const PORT = parseInt(process.env.PORT || '3000', 10);

startServer({ port: PORT })
    .then(() => {
        console.log(`topic-orchestration listening on ${PORT}`);
    })
    .catch((err) => {
        console.error('Failed to start server:', err);
        process.exit(1);
    });
