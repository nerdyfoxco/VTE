import express, { Request, Response, Router } from 'express';
import { PrismaClient } from '../../../../foundation/node_modules/@prisma/client';
import { requireAuth, requireRole, AuthenticatedRequest } from '../../../../foundation/src/security/middleware';

export const rulesRouter: Router = express.Router();
const prisma = new PrismaClient();

/**
 * [GET] /api/v1/rules
 * Fetch all policies and nested rules for the strictly authenticated Tenant.
 */
rulesRouter.get('/rules',
    requireAuth as any,
    requireRole(['admin', 'super_admin']) as any,
    async (req: Request, res: Response) => {
        try {
            const authReq = req as unknown as AuthenticatedRequest;
            const policies = await prisma.policyVersion.findMany({
                where: { tenantId: authReq.user.tenantId },
                include: { rules: true }
            });
            res.status(200).json(policies);
        } catch (error) {
            console.error("[RULES_API_FAULT]", error);
            res.status(500).json({ error: "Failed to fetch policies." });
        }
    }
);

/**
 * [POST] /api/v1/rules
 * Create a new dynamic rule mapped to a specific policy.
 */
rulesRouter.post('/rules',
    requireAuth as any,
    requireRole(['admin', 'super_admin']) as any,
    async (req: Request, res: Response) => {
        try {
            const authReq = req as unknown as AuthenticatedRequest;
            const { policyId, priority, conditionType, conditionValue, action, actionPayload } = req.body;

            // Verify Tenant owns the policy
            const policy = await prisma.policyVersion.findUnique({ where: { id: policyId } });
            if (!policy || policy.tenantId !== authReq.user.tenantId) {
                return res.status(403).json({ error: "FORBIDDEN", message: "Policy mismatch." });
            }

            const rule = await prisma.decisionRule.create({
                data: {
                    policyId,
                    priority: parseInt(priority, 10) || 100,
                    conditionType,
                    conditionValue,
                    action,
                    actionPayload
                }
            });
            res.status(201).json(rule);

        } catch (error) {
            console.error("[RULES_API_FAULT]", error);
            res.status(500).json({ error: "Failed to insert decision table row." });
        }
    }
);
