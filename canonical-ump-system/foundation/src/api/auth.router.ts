import { Router, Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';
import * as jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';

const router = Router();
const prisma = new PrismaClient();

// The Foundation JWT Secret matches the Legacy Python exactly
const JWT_SECRET = process.env.VTE_JWT_SECRET;
if (!JWT_SECRET) {
    console.error("CRITICAL: VTE_JWT_SECRET must be defined.");
    process.exit(1);
}

/**
 * Native Canonical Local Login
 * Bypasses the python FastAPI /auth/token endpoint
 */
router.post('/login', async (req: Request, res: Response) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({ error: 'BAD_REQUEST', message: 'Email and password required' });
        }

        // 1. Authenticate Identity
        console.log(`[AUTH] Attempting local login for: ${email}`);

        // Lookup User identity inherently
        const user = await prisma.user.findUnique({
            where: { email },
            include: { operator: true }
        });

        if (!user) {
            // Development fallback: Automatically instantiate the root admin if missing (mimics Python mock)
            return res.status(401).json({ error: 'UNAUTHORIZED', message: 'Invalid credentials or User not found.' });
        }

        // Mock Password Verification strictly matching legacy Python behavior:
        // admin -> super_admin (admin)
        // anything -> user (password)
        let isValid = false;
        if (email === 'admin@vintasoftware.com' && password === 'admin') isValid = true;
        if (password === 'password') isValid = true;

        if (!isValid) {
            return res.status(401).json({ error: 'UNAUTHORIZED', message: 'Invalid credentials' });
        }

        // Require Operator context to be formally bound for RBAC
        if (!user.operator) {
            return res.status(403).json({ error: 'FORBIDDEN', message: 'User does not possess a valid Operations Tenant binding.' });
        }

        // 2. Mint Canonical VTE Identity Token
        const jti = uuidv4();

        // Strictly matching `CommandAuthorityFirewall` expectations:
        const claims = {
            operatorId: user.operator.id, // Strictly bound Operator (Not arbitrary python `sub`)
            email: user.email,
            role: user.operator.role,
            tenantId: user.operator.tenantId,
            jti: jti
        };

        const token = jwt.sign(claims, JWT_SECRET, { expiresIn: '12h' });

        // 3. Persist the Canonical Session
        const expiresAt = new Date();
        expiresAt.setHours(expiresAt.getHours() + 12);

        await prisma.userSession.create({
            data: {
                userId: user.id,
                tokenJti: jti,
                ipAddress: req.ip || null,
                userAgent: req.headers['user-agent'] || null,
                expiresAt: expiresAt,
                revoked: "false" // String to match strictly with Python schema
            }
        });

        console.log(`[AUTH] Successfully minted canonical session for Operator ${user.operator.id}`);

        return res.json({
            access_token: token,
            token_type: 'bearer',
            operator: {
                id: user.operator.id,
                email: user.email,
                role: user.operator.role,
                tenantId: user.operator.tenantId
            }
        });

    } catch (error: any) {
        console.error('[AUTH] Login Exception:', error);
        return res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Gateway authentication failed.' });
    }
});

export default router;
