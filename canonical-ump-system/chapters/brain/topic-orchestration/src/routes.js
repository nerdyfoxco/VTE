"use strict";
// Canonical UMP Framework - Brain (Orchestration Router)
// Explicit REST entrypoints protected strictly by the Command Authority Firewall.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.orchestrationRouter = void 0;
const express_1 = __importDefault(require("express"));
const zod_1 = require("zod");
const client_1 = require("@prisma/client");
const middleware_1 = require("../../../../foundation/src/security/middleware");
const validator_1 = require("../../../kidney/topic-validation/src/validator");
const shadow_1 = require("./shadow");
exports.orchestrationRouter = express_1.default.Router();
const shadowEngine = new shadow_1.ShadowExecutionEngine();
/**
 * UMP Contract Schema: Determines the strict shape of a Workflow Request.
 */
const WorkflowExecutionSchema = zod_1.z.object({
    workflowName: zod_1.z.string().min(3),
    payload: zod_1.z.any()
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
exports.orchestrationRouter.post('/shadow', middleware_1.requireAuth, (0, middleware_1.requireRole)(['admin', 'operator']), (0, validator_1.validatePayload)(WorkflowExecutionSchema), async (req, res) => {
    // At this layer, TypeScript and Zod guarantee the shape and auth of these objects.
    const authReq = req;
    const tenantId = authReq.vteContext.tenantId;
    const operatorId = authReq.vteContext.operatorId;
    const validatedWorkflow = req.body;
    try {
        const shadowResult = await shadowEngine.routeInShadowMode(tenantId, operatorId, validatedWorkflow);
        res.status(200).json({
            message: "Shadow Execution Simulated Successfully",
            ...shadowResult
        });
    }
    catch (error) {
        console.error(`[SHADOW_FAILURE] Engine crashed for Tenant ${tenantId}:`, error);
        res.status(500).json({
            error: "SHADOW_ENGINE_FAULT",
            message: "The shadow evaluation encountered a fatal logical fault internally."
        });
    }
});
/**
 * [POST] /api/v1/orchestration/live
 *
 * Pipeline:
 * 1. requireAuth (Validates JWT)
 * 2. requireRole (Ensures the Operator has Execution rights)
 * 3. validatePayload (Kidney drops malicious keys and guarantees Contract shape)
 * 4. ShadowExecutionEngine (Writes explicitly LIVE deterministic traces AND drops Side-Effects to Hands)
 */
exports.orchestrationRouter.post('/live', middleware_1.requireAuth, (0, middleware_1.requireRole)(['admin', 'operator']), (0, validator_1.validatePayload)(WorkflowExecutionSchema), async (req, res) => {
    const authReq = req;
    const tenantId = authReq.vteContext.tenantId;
    const operatorId = authReq.vteContext.operatorId;
    const validatedWorkflow = req.body;
    try {
        const liveResult = await shadowEngine.routeInLiveMode(tenantId, operatorId, validatedWorkflow);
        res.status(200).json({
            message: "Live Execution Dispatched Successfully",
            ...liveResult
        });
    }
    catch (error) {
        console.error(`[LIVE_FAILURE] Engine crashed for Tenant ${tenantId}:`, error);
        res.status(500).json({
            error: "LIVE_ENGINE_FAULT",
            message: "The live evaluation encountered a fatal logical fault internally."
        });
    }
});
const prisma = new client_1.PrismaClient();
/**
 * [GET] /api/v1/orchestration/traces
 *
 * Fetches the canonical execution traces for telemetry dashboard mapping.
 * Strictly limited to administrative operators.
 */
exports.orchestrationRouter.get('/traces', middleware_1.requireAuth, (0, middleware_1.requireRole)(['admin']), async (req, res) => {
    try {
        const traces = await prisma.executionTrace.findMany({
            orderBy: { createdAt: 'desc' },
            take: 100
        });
        res.status(200).json(traces);
    }
    catch (error) {
        console.error(`[TELEMETRY_FAILURE] Failed to fetch traces:`, error);
        res.status(500).json({
            error: "TELEMETRY_ENGINE_FAULT",
            message: "Could not retrieve canonical execution traces."
        });
    }
});
