import * as jwt from 'jsonwebtoken';
import { CommandAuthorityFirewall } from '../src/security/firewall';

describe('CommandAuthorityFirewall', () => {
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

    describe('Initialization', () => {
        it('should halt boot sequence if VTE_JWT_SECRET is missing', () => {
            delete process.env.VTE_JWT_SECRET;
            expect(() => new CommandAuthorityFirewall()).toThrow('CRITICAL: VTE_JWT_SECRET environment variable is not defined.');
            process.env.VTE_JWT_SECRET = MOCK_SECRET; // Restore
        });

        it('should initialize successfully with a secret', () => {
            expect(() => new CommandAuthorityFirewall()).not.toThrow();
        });
    });

    describe('validateRequest', () => {
        let firewall: CommandAuthorityFirewall;

        beforeEach(() => {
            firewall = new CommandAuthorityFirewall();
        });

        it('should hard reject if Authorization header is missing', () => {
            expect(() => firewall.validateRequest(undefined)).toThrow('UNAUTHORIZED: Missing or malformed Authorization header.');
        });

        it('should hard reject if Authorization header is malformed', () => {
            expect(() => firewall.validateRequest('Basic invalid')).toThrow('UNAUTHORIZED: Missing or malformed Authorization header.');
        });

        it('should hard reject if token verification fails', () => {
            const badToken = jwt.sign({ tenantId: '123' }, 'wrong-secret');
            expect(() => firewall.validateRequest(`Bearer ${badToken}`)).toThrow(/UNAUTHORIZED: Token validation failed -/);
        });

        it('should hard reject if required claims are missing', () => {
            const missingRoleToken = generateMockToken({
                tenantId: '123',
                operatorId: 'ops-1'
                // Missing role and email
            });
            expect(() => firewall.validateRequest(`Bearer ${missingRoleToken}`)).toThrow('UNAUTHORIZED: JWT missing required VTE claims.');
        });

        it('should extract strictly validated AuthContext from valid JWT', () => {
            const validPayload = {
                tenantId: 'tenant-1',
                operatorId: 'ops-1',
                role: 'approver',
                email: 'test@nerdyfox.co'
            };
            const validToken = generateMockToken(validPayload);

            const context = firewall.validateRequest(`Bearer ${validToken}`);
            expect(context).toStrictEqual(validPayload);
        });
    });

    describe('enforceRBAC', () => {
        let firewall: CommandAuthorityFirewall;

        beforeEach(() => {
            firewall = new CommandAuthorityFirewall();
        });

        it('should allow access if role is present in allowed array', () => {
            const context = {
                tenantId: 't-1',
                operatorId: 'ops-1',
                role: 'admin',
                email: 'admin@test.com'
            };
            expect(() => firewall.enforceRBAC(context, ['admin', 'super-admin'])).not.toThrow();
        });

        it('should reject access if role is missing from allowed array', () => {
            const context = {
                tenantId: 't-1',
                operatorId: 'ops-1',
                role: 'viewer',
                email: 'viewer@test.com'
            };
            expect(() => firewall.enforceRBAC(context, ['admin', 'approver'])).toThrow(/FORBIDDEN: Operator role 'viewer' is not authorized/);
        });
    });
});
