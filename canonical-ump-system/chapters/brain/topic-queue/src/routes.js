"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.queueRouter = void 0;
const express_1 = __importDefault(require("express"));
const client_1 = require("../../../../foundation/node_modules/@prisma/client");
const middleware_1 = require("../../../../foundation/src/security/middleware");
exports.queueRouter = express_1.default.Router();
const prisma = new client_1.PrismaClient();
/**
 * [GET] /api/v1/queue
 *
 * Replaces the Python `get_queue_items` endpoint.
 * Natively supports sorting, filtering, and pagination using Prisma,
 * securely scoped by the `requireAuth` JWT validation layer.
 */
exports.queueRouter.get('/queue', middleware_1.requireAuth, async (req, res) => {
    try {
        const authReq = req;
        // Extract query params mirroring Python contract
        const skip = parseInt(req.query.skip) || 0;
        const limit = parseInt(req.query.limit) || 10;
        const sortBy = req.query.sort_by || 'priority';
        const order = req.query.order || 'asc';
        const status = req.query.status;
        const priority = req.query.priority ? parseInt(req.query.priority) : undefined;
        const search = req.query.search;
        // Security: Allowlist sort fields (identical to Python)
        const allowedSorts = ["priority", "slaDeadline", "title", "createdAt"];
        // Map legacy sort_by to Prisma fields
        const sortMap = {
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
        const whereClause = {};
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
    }
    catch (error) {
        console.error("[QUEUE_ROUTER_FAULT]", error);
        res.status(500).json({ error: "INTERNAL_SERVER_ERROR", message: "Failed to resolve queue items." });
    }
});
