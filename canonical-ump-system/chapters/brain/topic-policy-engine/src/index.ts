import { startServer } from './server';

const PORT = parseInt(process.env.PORT || '3001', 10);

startServer({ port: PORT })
    .then(({ port }) => {
        console.log(`topic-policy-engine listening on ${port}`);
    })
    .catch((err) => {
        console.error(`Failed to start topic-policy-engine:`, err);
        process.exit(1);
    });
