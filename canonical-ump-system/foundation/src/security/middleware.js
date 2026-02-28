"use strict";
// Canonical UMP Framework - Express Auth Middleware
// Secures Express.js/Next.js routes using the Command Authority Firewall
Object.defineProperty(exports, "__esModule", { value: true });
exports.requireRole = exports.requireAuth = void 0;
const firewall_1 = require("./firewall");
let firewall;
const getFirewall = () => {
    if (!firewall) {
        firewall = new firewall_1.CommandAuthorityFirewall();
    }
    return firewall;
};
/**
 * Validates the Authorization header and attaches the AuthContext to the request.
 * Hard rejects any request mapping to a 401 Unauthorized if invalid.
 */
const requireAuth = (req, res, next) => {
    try {
        const authHeader = req.headers.authorization;
        const context = getFirewall().validateRequest(authHeader);
        // Attach deterministic context for downstream Organs
        req.vteContext = context;
        next();
    }
    catch (error) {
        console.error(`[AUTH_FAILURE] Route: ${req.url} - Error: ${error.message}`);
        res.status(401).json({
            error: "UNAUTHORIZED",
            message: error.message
        });
    }
};
exports.requireAuth = requireAuth;
/**
 * Higher-order middleware enforcing Role-Based Access Control via CAF.
 * Must be used AFTER requireAuth.
 */
const requireRole = (allowedRoles) => {
    return (req, res, next) => {
        const authReq = req;
        if (!authReq.vteContext) {
            return res.status(500).json({ error: "INTERNAL_ERROR", message: "requireRole invoked before requireAuth" });
        }
        try {
            getFirewall().enforceRBAC(authReq.vteContext, allowedRoles);
            next();
        }
        catch (error) {
            console.error(`[RBAC_FAILURE] Operator ${authReq.vteContext.operatorId} barred from Route: ${req.url}`);
            res.status(403).json({
                error: "FORBIDDEN",
                message: error.message
            });
        }
    };
};
exports.requireRole = requireRole;
