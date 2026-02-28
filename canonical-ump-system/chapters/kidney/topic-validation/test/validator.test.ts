import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { validatePayload } from '../src/validator';

describe('Kidney Validator Middleware', () => {
    // Define a deterministic mock schema following UMP rules
    const UserSchema = z.object({
        tenantId: z.string().uuid(),
        email: z.string().email(),
        retries: z.number().min(0).max(3).optional()
    });

    const mockRequest = (body: any): Partial<Request> => ({
        body,
        url: '/api/v1/users'
    });

    const mockResponse = (): Partial<Response> => {
        const res: any = {};
        res.status = jest.fn().mockReturnValue(res);
        res.json = jest.fn().mockReturnValue(res);
        return res;
    };

    it('should pass validation and call next() for a valid payload', async () => {
        const validBody = {
            tenantId: '123e4567-e89b-12d3-a456-426614174000',
            email: 'test@nerdyfox.co',
            retries: 2
        };
        const req = mockRequest(validBody) as Request;
        const res = mockResponse() as Response;
        const next = jest.fn();

        const middleware = validatePayload(UserSchema);
        await middleware(req, res, next);

        expect(next).toHaveBeenCalled();
        expect(res.status).not.toHaveBeenCalled();
        // Ensure body is untouched (or rather, safely parsed)
        expect(req.body).toStrictEqual(validBody);
    });

    it('should strip unknown keys automatically in the validated payload', async () => {
        const payloadWithJunk = {
            tenantId: '123e4567-e89b-12d3-a456-426614174000',
            email: 'test@nerdyfox.co',
            maliciousKey: 'drop_tables();'
        };
        const req = mockRequest(payloadWithJunk) as Request;
        const res = mockResponse() as Response;
        const next = jest.fn();

        const middleware = validatePayload(UserSchema);
        await middleware(req, res, next);

        expect(next).toHaveBeenCalled();
        // The maliciousKey should have been stripped by Zod parsing strictly
        expect(req.body).not.toHaveProperty('maliciousKey');
        expect(req.body.email).toBe('test@nerdyfox.co');
    });

    it('should return 400 Bad Request with deterministic violations on invalid data', async () => {
        const invalidBody = {
            tenantId: 'not-a-uuid',
            email: 'invalid-email',
            retries: 5 // Over the max of 3
        };
        const req = mockRequest(invalidBody) as Request;
        const res = mockResponse() as Response;
        const next = jest.fn();

        const middleware = validatePayload(UserSchema);
        await middleware(req, res, next);

        expect(next).not.toHaveBeenCalled();
        expect(res.status).toHaveBeenCalledWith(400);

        // Assert the exact taxonomic shape of the error response
        expect(res.json).toHaveBeenCalledWith(expect.objectContaining({
            error: 'BAD_REQUEST',
            message: 'Payload schema validation failed.',
            violations: expect.arrayContaining([
                expect.objectContaining({ path: 'tenantId' }),
                expect.objectContaining({ path: 'email' }),
                expect.objectContaining({ path: 'retries' })
            ])
        }));
    });
});
