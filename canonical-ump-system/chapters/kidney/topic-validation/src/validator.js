"use strict";
// Canonical UMP Framework - Kidney (Validation Organ)
// Asserts all incoming payloads against explicit JSON schemas (Zod) before Orchestration
Object.defineProperty(exports, "__esModule", { value: true });
exports.validatePayload = void 0;
const zod_1 = require("zod");
/**
 * Higher-order middleware that intercepts an Express request body
 * and validates it deterministically against a Zod schema.
 *
 * If validation fails, it halts execution and returns a structured 400 Bad Request
 * containing the exact path and nature of the schema violation.
 */
const validatePayload = (schema) => {
    return async (req, res, next) => {
        try {
            // Assert the body perfectly matches the schema (strips unknown keys automatically if configured)
            const validatedData = await schema.parseAsync(req.body);
            // Overwrite the request body with the explicitly validated, type-safe payload
            req.body = validatedData;
            next();
        }
        catch (error) {
            if (error instanceof zod_1.ZodError || error?.name === 'ZodError') {
                console.error(`[VALIDATION_FATAL] Bad Request on ${req.url}`);
                res.status(400).json({
                    error: "BAD_REQUEST",
                    message: "Payload schema validation failed.",
                    violations: error.errors.map((e) => ({
                        path: e.path.join('.'),
                        issue: e.message
                    }))
                });
            }
            else {
                console.error(`[VALIDATION_SYSTEM_ERROR] ${error}`);
                res.status(500).json({
                    error: "INTERNAL_ERROR",
                    message: "A systemic exception occurred during payload validation."
                });
            }
        }
    };
};
exports.validatePayload = validatePayload;
