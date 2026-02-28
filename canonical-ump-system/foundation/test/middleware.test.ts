import { Request, Response, NextFunction } from 'express';
import * as jwt from 'jsonwebtoken';
import { requireAuth, requireRole, AuthenticatedRequest } from '../src/security/middleware';

describe('Auth Middleware', () => {
    const MOCK_SECRET = 'test-secret-12345';
    let originalEnv: NodeJS.ProcessEnv;

    beforeAll(() => {
        originalEnv = process.env;
        process.env.VTE_JWT_SECRET = MOCK_SECRET;
    });

    afterAll(() => {
        process.env = originalEnv;
    });

    const generateMockToken = (payload: any) => {
        return jwt.sign(payload, MOCK_SECRET);
    };

    const mockRequest = (headers: any = {}): Partial<Request> => ({
        headers,
        url: '/api/v1/test'
    });

    const mockResponse = (): Partial<Response> => {
        const res: any = {};
        res.status = jest.fn().mockReturnValue(res);
        res.json = jest.fn().mockReturnValue(res);
        return res;
    };

    describe('requireAuth', () => {
        it('should return 401 if Authorization header is missing', () => {
            const req = mockRequest();
            const res = mockResponse();
            const next = jest.fn();

            requireAuth(req as Request, res as Response, next);

            expect(res.status).toHaveBeenCalledWith(401);
            expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ error: 'UNAUTHORIZED' }));
            expect(next).not.toHaveBeenCalled();
        });

        it('should return 401 if token is invalid', () => {
            const req = mockRequest({ authorization: 'Bearer bad-token' });
            const res = mockResponse();
            const next = jest.fn();

            requireAuth(req as Request, res as Response, next);

            expect(res.status).toHaveBeenCalledWith(401);
            expect(req).not.toHaveProperty('vteContext');
            expect(next).not.toHaveBeenCalled();
        });

        it('should attach vteContext and call next() on valid token', () => {
            const payload = {
                tenantId: 't-1',
                operatorId: 'ops-1',
                role: 'admin',
                email: 'test@nerdyfox.co'
            };
            const token = generateMockToken(payload);
            const req = mockRequest({ authorization: `Bearer ${token}` });
            const res = mockResponse();
            const next = jest.fn();

            requireAuth(req as Request, res as Response, next);

            expect(next).toHaveBeenCalled();
            expect((req as AuthenticatedRequest).vteContext).toStrictEqual(payload);
        });
    });

    describe('requireRole', () => {
        it('should return 500 if requireRole is called before requireAuth', () => {
            const req = mockRequest();
            const res = mockResponse();
            const next = jest.fn();

            const middleware = requireRole(['admin']);
            middleware(req as Request, res as Response, next);

            expect(res.status).toHaveBeenCalledWith(500);
            expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ error: 'INTERNAL_ERROR' }));
            expect(next).not.toHaveBeenCalled();
        });

        it('should return 403 if role is forbidden', () => {
            const req = mockRequest();
            (req as AuthenticatedRequest).vteContext = {
                tenantId: 't-1',
                operatorId: 'ops-1',
                role: 'viewer',
                email: 'test@nerdyfox.co'
            };
            const res = mockResponse();
            const next = jest.fn();

            const middleware = requireRole(['admin', 'approver']);
            middleware(req as Request, res as Response, next);

            expect(res.status).toHaveBeenCalledWith(403);
            expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ error: 'FORBIDDEN' }));
            expect(next).not.toHaveBeenCalled();
        });

        it('should call next() if role is permitted', () => {
            const req = mockRequest();
            (req as AuthenticatedRequest).vteContext = {
                tenantId: 't-1',
                operatorId: 'ops-1',
                role: 'admin',
                email: 'test@nerdyfox.co'
            };
            const res = mockResponse();
            const next = jest.fn();

            const middleware = requireRole(['admin']);
            middleware(req as Request, res as Response, next);

            expect(next).toHaveBeenCalled();
        });
    });
});
