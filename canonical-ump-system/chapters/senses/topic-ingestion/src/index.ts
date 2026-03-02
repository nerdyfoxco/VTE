import { SensesPoller } from './poller';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Load the root `.env` securely for cross-tenant gateway secrets
dotenv.config({ path: path.resolve(__dirname, '../../../../../.env') });

const poller = new SensesPoller();
const POLL_INTERVAL = process.env.POLLING_INTERVAL_MS ? parseInt(process.env.POLLING_INTERVAL_MS) : 15000; // Default 15s for testing

console.log("[SENSES] Starting Phase 14 Native Ingestion Engine...");
console.log(`[SENSES] Gateway target: ${process.env.GATEWAY_URL || 'http://localhost:8000/api/v1/orchestration/live'}`);

// Initialize the continuous polling hook internally
poller.start(POLL_INTERVAL);

// Handle graceful engine halts
process.on('SIGINT', () => {
    poller.stop();
    process.exit(0);
});

process.on('SIGTERM', () => {
    poller.stop();
    process.exit(0);
});
