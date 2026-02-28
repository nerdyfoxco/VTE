"use strict";
// Canonical UMP Framework - Command Authority Firewall (CAF)
// Enforces synchronous RBAC and JWT validation before Orchestration Brain execution.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.CommandAuthorityFirewall = void 0;
const jwt = __importStar(require("jsonwebtoken"));
class CommandAuthorityFirewall {
    jwtSecret;
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
    validateRequest(authHeader) {
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            throw new Error("UNAUTHORIZED: Missing or malformed Authorization header.");
        }
        const token = authHeader.split(' ')[1];
        try {
            const decoded = jwt.verify(token, this.jwtSecret);
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
        }
        catch (error) {
            throw new Error(`UNAUTHORIZED: Token validation failed - ${error.message}`);
        }
    }
    /**
     * Enforces Role-Based Access Control against a given context.
     * @param context The authenticated context
     * @param allowedRoles Array of roles permitted to execute the command.
     */
    enforceRBAC(context, allowedRoles) {
        if (!allowedRoles.includes(context.role)) {
            throw new Error(`FORBIDDEN: Operator role '${context.role}' is not authorized to execute this command. Required roles: [${allowedRoles.join(', ')}]`);
        }
    }
}
exports.CommandAuthorityFirewall = CommandAuthorityFirewall;
