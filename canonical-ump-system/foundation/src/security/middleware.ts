// Canonical UMP Framework - Express Auth Middleware
// Secures Express.js/Next.js routes using the Command Authority Firewall

import { Request, Response, NextFunction } from 'express';
import { CommandAuthorityFirewall, AuthContext } from './firewall';

// Extend Express Request to include strictly validated AuthContext
export interface AuthenticatedRequest extends Request {
    vteContext: AuthContext;
}

let firewall: CommandAuthorityFirewall;

const getFirewall = () => {
    if (!firewall) {
        firewall = new CommandAuthorityFirewall();
    }
    return firewall;
};

/**
 * Validates the Authorization header and attaches the AuthContext to the request.
 * Hard rejects any request mapping to a 401 Unauthorized if invalid.
 */
export const requireAuth = (req: Request, res: Response, next: NextFunction) => {
    try {
        const authHeader = req.headers.authorization;
        const context = getFirewall().validateRequest(authHeader);

        // Attach deterministic context for downstream Organs
        (req as AuthenticatedRequest).vteContext = context;
        next();
    } catch (error: any) {
        console.error(`[AUTH_FAILURE] Route: ${req.url} - Error: ${error.message}`);
        res.status(401).json({
            error: "UNAUTHORIZED",
            message: error.message
        });
    }
};

/**
 * Higher-order middleware enforcing Role-Based Access Control via CAF.
 * Must be used AFTER requireAuth.
 */
export const requireRole = (allowedRoles: string[]) => {
    return (req: Request, res: Response, next: NextFunction) => {
        const authReq = req as AuthenticatedRequest;
        if (!authReq.vteContext) {
            return res.status(500).json({ error: "INTERNAL_ERROR", message: "requireRole invoked before requireAuth" });
        }

        try {
            getFirewall().enforceRBAC(authReq.vteContext, allowedRoles);
            next();
        } catch (error: any) {
            console.error(`[RBAC_FAILURE] Operator ${authReq.vteContext.operatorId} barred from Route: ${req.url}`);
            res.status(403).json({
                error: "FORBIDDEN",
                message: error.message
            });
        }
    };
};
