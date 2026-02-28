import express from 'express';
import supertest from 'supertest';
import * as jwt from 'jsonwebtoken';
import { orchestrationRouter } from '../src/routes';

// Mock the Shadow Execution Engine explicitly to prevent real instantiations/Prisma calls
jest.mock('../src/shadow', () => {
    return {
        ShadowExecutionEngine: jest.fn().mockImplementation(() => {
            return {
                routeInShadowMode: jest.fn().mockResolvedValue({
                    traceId: 'mock-trace-123',
                    mode: 'SHADOW',
                    status: 'SIMULATED_SUCCESS',
                    simulatedEffects: []
                })
            };
        })
    };
});

const app = express();
app.use(express.json());
app.use('/api/v1/orchestration', orchestrationRouter);

describe('Orchestration Router (Trace Telemetry)', () => {
    const MOCK_SECRET = 'test-shadow-secret-123';
    let originalEnv: NodeJS.ProcessEnv;

    beforeAll(() => {
        originalEnv = process.env;
        process.env.VTE_JWT_SECRET = MOCK_SECRET;
    });

    afterAll(() => {
        process.env = originalEnv;
    });

    const generateToken = (role: string) => {
        return jwt.sign({
            tenantId: '123e4567-e89b-12d3-a456-426614174000',
            operatorId: 'ops-admin-1',
            role: role,
            email: 'admin@vte.test'
        }, MOCK_SECRET);
    };

    it('should reject unauthenticated requests via the CAF Middleware', async () => {
        const response = await supertest(app)
            .post('/api/v1/orchestration/shadow')
            .send({});

        expect(response.status).toBe(401);
        expect(response.body.error).toBe('UNAUTHORIZED');
    });

    it('should reject unauthorized roles via RBAC', async () => {
        const token = generateToken('viewer');
        const response = await supertest(app)
            .post('/api/v1/orchestration/shadow')
            .set('Authorization', `Bearer ${token}`)
            .send({ workflowName: 'Test', payload: {} });

        expect(response.status).toBe(403);
        expect(response.body.error).toBe('FORBIDDEN');
    });

    it('should intercept bad schemas via the Kidney Organ', async () => {
        const token = generateToken('admin');
        const response = await supertest(app)
            .post('/api/v1/orchestration/shadow')
            .set('Authorization', `Bearer ${token}`)
            .send({ badPayloadShape: true }); // Missing workflowName

        expect(response.status).toBe(400);
        expect(response.body.error).toBe('BAD_REQUEST');
        expect(response.body.violations[0].path).toBe('workflowName');
    });

    it('should execute Shadow Mode safely when authorized and valid', async () => {
        const token = generateToken('admin');
        const response = await supertest(app)
            .post('/api/v1/orchestration/shadow')
            .set('Authorization', `Bearer ${token}`)
            .send({
                workflowName: 'SendWeeklyReport',
                payload: { includeMetrics: true }
            });

        expect(response.status).toBe(200);
        expect(response.body.message).toBe('Shadow Execution Simulated Successfully');
        expect(response.body.traceId).toBe('mock-trace-123');
        expect(response.body.status).toBe('SIMULATED_SUCCESS');
    });
});
