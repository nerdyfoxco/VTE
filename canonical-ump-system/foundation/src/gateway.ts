import express from 'express';
import cors from 'cors';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { orchestrationRouter } from '../../chapters/brain/topic-orchestration/src/routes';
import { queueRouter } from '../../chapters/brain/topic-queue/src/routes';
import authRouter from './api/auth.router';

const app = express();
const PORT = process.env.PORT || 8000;
const LEGACY_PYTHON_BACKEND = process.env.LEGACY_BACKEND_URL || 'http://127.0.0.1:8001';

// 1. Universal Middlewares
app.use(cors({
    origin: '*',
    credentials: true,
}));

// We only parse JSON for our native routes. The proxy middleware needs 
// unmodified raw streams for the Python backend.
const jsonParser = express.json();

// 2. Canonical UMP Routes
console.log("[GATEWAY] 🟢 Mounting Canonical UMP Orchestration Router at /api/v1/orchestration");
app.use('/api/v1/orchestration', jsonParser, orchestrationRouter as any);

console.log("[GATEWAY] 🟢 Mounting Canonical UMP Queue Router at /api/v1");
app.use('/api/v1', jsonParser, queueRouter as any);

console.log("[GATEWAY] 🟢 Mounting Canonical UMP Authentication Router at /api/v1/auth");
app.use('/api/v1/auth', jsonParser, authRouter);

// 3. Strangler Fig Proxy (Catch-All)
console.log(`[GATEWAY] 🟠 Proxying remaining /api/v1/* traffic -> ${LEGACY_PYTHON_BACKEND}`);
app.use(
    '/api/v1',
    createProxyMiddleware({
        target: LEGACY_PYTHON_BACKEND,
        changeOrigin: true,
        pathRewrite: {
            '^/': '/api/v1/'
        }
    })
);

// 4. Initialization
app.listen(PORT, () => {
    console.log(`=========================================`);
    console.log(`🚀 Canonical UMP Gateway Started`);
    console.log(`📡 Listening fiercely on Port ${PORT}`);
    console.log(`=========================================`);
});
