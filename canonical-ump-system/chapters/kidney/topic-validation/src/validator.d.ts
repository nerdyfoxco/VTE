import { Request, Response, NextFunction } from 'express';
import { AnyZodObject } from 'zod';
/**
 * Higher-order middleware that intercepts an Express request body
 * and validates it deterministically against a Zod schema.
 *
 * If validation fails, it halts execution and returns a structured 400 Bad Request
 * containing the exact path and nature of the schema violation.
 */
export declare const validatePayload: (schema: AnyZodObject) => (req: Request, res: Response, next: NextFunction) => Promise<void>;
