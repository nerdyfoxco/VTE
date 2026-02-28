import express from 'express';
import cors from 'cors';
import { createProxyMiddleware } from 'http-proxy-middleware';

import { orchestrationRouter } from '../../../brain/topic-orchestration/src/routes';

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
if (orchestrationRouter) {
    console.log("[GATEWAY] 🟢 Mounting Canonical UMP Orchestration Router at /api/v1/orchestration");
    app.use('/api/v1/orchestration', jsonParser, orchestrationRouter);
}

// 3. Strangler Fig Proxy (Catch-All)
// All requests not matching the above explicitly defined Canonical paths are
// securely tunneled to the Python FastAPI backend on Port 8001.
console.log(`[GATEWAY] 🟠 Proxying remaining /api/v1/* traffic -> ${LEGACY_PYTHON_BACKEND}`);
app.use(
    '/api/v1',
    createProxyMiddleware({
        target: LEGACY_PYTHON_BACKEND,
        changeOrigin: true,
        logLevel: 'debug',
    })
);

// 4. Initialization
app.listen(PORT, () => {
    console.log(`=========================================`);
    console.log(`🚀 Canonical UMP Gateway Started`);
    console.log(`📡 Listening fiercely on Port ${PORT}`);
    console.log(`=========================================`);
});
