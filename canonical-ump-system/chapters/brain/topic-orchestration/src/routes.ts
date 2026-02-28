// Canonical UMP Framework - Brain (Orchestration Router)
// Explicit REST entrypoints protected strictly by the Command Authority Firewall.

import express, { Request, Response } from 'express';
import { z } from 'zod';
import { PrismaClient } from '@prisma/client';
import { requireAuth, requireRole, AuthenticatedRequest } from '../../../../foundation/src/security/middleware';
import { validatePayload } from '../../../kidney/topic-validation/src/validator';
import { ShadowExecutionEngine } from './shadow';

export const orchestrationRouter = express.Router();
const shadowEngine = new ShadowExecutionEngine();

/**
 * UMP Contract Schema: Determines the strict shape of a Workflow Request.
 */
const WorkflowExecutionSchema = z.object({
    workflowName: z.string().min(3),
    payload: z.any()
});

/**
 * [POST] /api/v1/orchestration/shadow
 * 
 * Pipeline:
 * 1. requireAuth (Validates JWT, halts if missing)
 * 2. requireRole (Ensures the Operator has Execution rights)
 * 3. validatePayload (Kidney drops malicious keys and guarantees Contract shape)
 * 4. ShadowExecutionEngine (Writes explicitly SHADOW deterministic traces without side effects)
 */
orchestrationRouter.post('/shadow',
    requireAuth as any,
    requireRole(['admin', 'operator']) as any,
    validatePayload(WorkflowExecutionSchema) as any,
    async (req: Request, res: Response) => {

        // At this layer, TypeScript and Zod guarantee the shape and auth of these objects.
        const authReq = req as unknown as AuthenticatedRequest;
        const tenantId = authReq.vteContext.tenantId;
        const operatorId = authReq.vteContext.operatorId;
        const validatedWorkflow = req.body;

        try {
            const shadowResult = await shadowEngine.routeInShadowMode(tenantId, operatorId, validatedWorkflow);

            res.status(200).json({
                message: "Shadow Execution Simulated Successfully",
                ...shadowResult
            });
        } catch (error: any) {
            console.error(`[SHADOW_FAILURE] Engine crashed for Tenant ${tenantId}:`, error);
            res.status(500).json({
                error: "SHADOW_ENGINE_FAULT",
                message: "The shadow evaluation encountered a fatal logical fault internally."
            });
        }
    }
);

/**
 * [POST] /api/v1/orchestration/live
 * 
 * Pipeline:
 * 1. requireAuth (Validates JWT)
 * 2. requireRole (Ensures the Operator has Execution rights)
 * 3. validatePayload (Kidney drops malicious keys and guarantees Contract shape)
 * 4. ShadowExecutionEngine (Writes explicitly LIVE deterministic traces AND drops Side-Effects to Hands)
 */
orchestrationRouter.post('/live',
    requireAuth as any,
    requireRole(['admin', 'operator']) as any,
    validatePayload(WorkflowExecutionSchema) as any,
    async (req: Request, res: Response) => {

        const authReq = req as unknown as AuthenticatedRequest;
        const tenantId = authReq.vteContext.tenantId;
        const operatorId = authReq.vteContext.operatorId;
        const validatedWorkflow = req.body;

        try {
            const liveResult = await shadowEngine.routeInLiveMode(tenantId, operatorId, validatedWorkflow);

            res.status(200).json({
                message: "Live Execution Dispatched Successfully",
                ...liveResult
            });
        } catch (error: any) {
            console.error(`[LIVE_FAILURE] Engine crashed for Tenant ${tenantId}:`, error);
            res.status(500).json({
                error: "LIVE_ENGINE_FAULT",
                message: "The live evaluation encountered a fatal logical fault internally."
            });
        }
    }
);

const prisma = new PrismaClient();

/**
 * [GET] /api/v1/orchestration/traces
 * 
 * Fetches the canonical execution traces for telemetry dashboard mapping.
 * Strictly limited to administrative operators.
 */
orchestrationRouter.get('/traces',
    requireAuth as any,
    requireRole(['admin']) as any,
    async (req: Request, res: Response) => {
        try {
            const traces = await prisma.executionTrace.findMany({
                orderBy: { createdAt: 'desc' },
                take: 100
            });
            res.status(200).json(traces);
        } catch (error: any) {
            console.error(`[TELEMETRY_FAILURE] Failed to fetch traces:`, error);
            res.status(500).json({
                error: "TELEMETRY_ENGINE_FAULT",
                message: "Could not retrieve canonical execution traces."
            });
        }
    }
);
