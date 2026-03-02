import { Queue, Worker, QueueEvents, ConnectionOptions } from 'bullmq';
import IORedis from 'ioredis';

/**
 * Configure standard Redis Connection for the UMP System.
 * Connects to the primary spine-redis container defined in docker-compose.
 */
const redisConnection: ConnectionOptions = {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379', 10),
};

// Create a reusable underlying ioredis connection to avoid connection limits
export const connection = new IORedis(redisConnection);

/**
 * Instantiate standard Queue references for the Brain, Senses, and Hands.
 */
export const IngestionQueue = new Queue('ingestion-queue', { connection });
export const OrchestrationQueue = new Queue('orchestration-queue', { connection });
export const DispatchQueue = new Queue('dispatch-queue', { connection });

/**
 * Instantiate specific Queue Events to allow pub/sub listeners.
 */
export const IngestionQueueEvents = new QueueEvents('ingestion-queue', { connection });
export const OrchestrationQueueEvents = new QueueEvents('orchestration-queue', { connection });
export const DispatchQueueEvents = new QueueEvents('dispatch-queue', { connection });

console.log("[BULLMQ_INIT] Successfully initialized canonical message queues over Redis.");
