import { PrismaClient } from '@prisma/client';
import { mockDeep, mockReset, DeepMockProxy } from 'jest-mock-extended';
import { ShadowExecutionEngine, WorkflowRequest } from '../src/shadow';

jest.mock('@prisma/client', () => ({
    PrismaClient: jest.fn()
}));

describe('ShadowExecutionEngine', () => {
    let engine: ShadowExecutionEngine;
    let prismaMock: DeepMockProxy<PrismaClient>;

    beforeEach(() => {
        prismaMock = mockDeep<PrismaClient>();
        (PrismaClient as jest.Mock).mockImplementation(() => prismaMock);
        engine = new ShadowExecutionEngine();
    });

    afterEach(() => {
        mockReset(prismaMock);
    });

    it('should calculate projected effects and commit a SHADOW_VALIDATED trace to Prisma', async () => {
        const tenantId = 't-uuid-1';
        const operatorId = 'ops-1';
        const request: WorkflowRequest = {
            workflowName: 'TestE2EWorkflow',
            payload: { mock: 'data' }
        };

        const mockTraceResult = {
            id: 'trace-1234',
            tenantId,
            operatorId,
            state: 'SHADOW_VALIDATED',
            contextSnapshot: {},
            createdAt: new Date(),
            completedAt: null,
            errorHash: null
        };

        // Mock the resolved value from Prisma
        prismaMock.executionTrace.create.mockResolvedValue(mockTraceResult as any);

        const result = await engine.routeInShadowMode(tenantId, operatorId, request);

        // Verify Prisma was called correctly to ensure SHADOW traces never mutate into LIVE states
        expect(prismaMock.executionTrace.create).toHaveBeenCalledWith({
            data: {
                tenantId: tenantId,
                operatorId: operatorId,
                state: 'SHADOW_VALIDATED',
                contextSnapshot: expect.objectContaining({
                    originalRequest: request,
                    projectedEffects: expect.any(Array)
                })
            }
        });

        // Verify the logic halts side effects and explicitly tags the model
        expect(result.mode).toBe('SHADOW');
        expect(result.status).toBe('SIMULATED_SUCCESS');
        expect(result.simulatedEffects).toBeInstanceOf(Array);
        expect(result.simulatedEffects[0].target).toBe('SENDGRID_API'); // Based on mock logic
    });
});
