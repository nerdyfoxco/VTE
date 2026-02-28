// Canonical UMP Framework - Command Authority Firewall (CAF)
// Enforces synchronous RBAC and JWT validation before Orchestration Brain execution.

import * as jwt from 'jsonwebtoken';

export interface AuthContext {
    tenantId: string;
    operatorId: string;
    role: string;
    email: string;
}

export class CommandAuthorityFirewall {
    private readonly jwtSecret: string;

    constructor() {
        const secret = process.env.VTE_JWT_SECRET;
        if (!secret) {
            // Institutional Over-Safety Bias: Halt if secure configuration is missing.
            throw new Error("CRITICAL: VTE_JWT_SECRET environment variable is not defined. Halting boot sequence.");
        }
        this.jwtSecret = secret;
    }

    /**
     * Validates an incoming authorization header and extracts the operator context.
     * @param authHeader The raw `Authorization: Bearer <token>` header
     * @returns AuthContext if valid
     * @throws Error if token is missing, invalid, or expired.
     */
    public validateRequest(authHeader?: string): AuthContext {
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            throw new Error("UNAUTHORIZED: Missing or malformed Authorization header.");
        }

        const token = authHeader.split(' ')[1];

        try {
            const decoded = jwt.verify(token, this.jwtSecret) as any;

            // Ensure minimum required claims are present
            if (!decoded.tenantId || !decoded.operatorId || !decoded.role || !decoded.email) {
                throw new Error("UNAUTHORIZED: JWT missing required VTE claims.");
            }

            return {
                tenantId: decoded.tenantId,
                operatorId: decoded.operatorId,
                role: decoded.role,
                email: decoded.email
            };
        } catch (error: any) {
            throw new Error(`UNAUTHORIZED: Token validation failed - ${error.message}`);
        }
    }

    /**
     * Enforces Role-Based Access Control against a given context.
     * @param context The authenticated context
     * @param allowedRoles Array of roles permitted to execute the command.
     */
    public enforceRBAC(context: AuthContext, allowedRoles: string[]): void {
        if (!allowedRoles.includes(context.role)) {
            throw new Error(`FORBIDDEN: Operator role '${context.role}' is not authorized to execute this command. Required roles: [${allowedRoles.join(', ')}]`);
        }
    }
}
