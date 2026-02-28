import express, { Request, Response } from 'express';
import { PrismaClient } from '../../../../foundation/node_modules/@prisma/client';
import { requireAuth, AuthenticatedRequest } from '../../../../foundation/src/security/middleware';

export const queueRouter = express.Router();
const prisma = new PrismaClient();

/**
 * [GET] /api/v1/queue
 * 
 * Replaces the Python `get_queue_items` endpoint.
 * Natively supports sorting, filtering, and pagination using Prisma,
 * securely scoped by the `requireAuth` JWT validation layer.
 */
queueRouter.get('/queue',
    requireAuth as any,
    async (req: Request, res: Response) => {
        try {
            const authReq = req as unknown as AuthenticatedRequest;

            // Extract query params mirroring Python contract
            const skip = parseInt(req.query.skip as string) || 0;
            const limit = parseInt(req.query.limit as string) || 10;
            const sortBy = (req.query.sort_by as string) || 'priority';
            const order = (req.query.order as string) || 'asc';

            const status = req.query.status as string | undefined;
            const priority = req.query.priority ? parseInt(req.query.priority as string) : undefined;
            const search = req.query.search as string | undefined;

            // Security: Allowlist sort fields (identical to Python)
            const allowedSorts = ["priority", "slaDeadline", "title", "createdAt"];
            // Map legacy sort_by to Prisma fields
            const sortMap: Record<string, string> = {
                "priority": "priority",
                "sla_deadline": "slaDeadline",
                "title": "title",
                "created_at": "createdAt"
            };

            const prismaSortField = sortMap[sortBy];
            if (!prismaSortField) {
                return res.status(400).json({ detail: `Invalid sort_by field. Allowed: ${Object.keys(sortMap)}` });
            }

            // Build Where clause natively using Prisma
            const whereClause: any = {};

            if (status && status.toUpperCase() !== 'ALL') {
                whereClause.status = status.toUpperCase();
            }
            if (priority !== undefined) {
                whereClause.priority = priority;
            }
            if (search && search.trim() !== '') {
                whereClause.title = {
                    contains: search,
                    mode: 'insensitive' // Maps to ilike
                };
            }

            // Fetch Items
            const items = await prisma.queueItem.findMany({
                where: whereClause,
                orderBy: {
                    [prismaSortField]: order === 'desc' ? 'desc' : 'asc'
                },
                skip,
                take: limit
            });

            res.status(200).json(items);

        } catch (error) {
            console.error("[QUEUE_ROUTER_FAULT]", error);
            res.status(500).json({ error: "INTERNAL_SERVER_ERROR", message: "Failed to resolve queue items." });
        }
    }
);
