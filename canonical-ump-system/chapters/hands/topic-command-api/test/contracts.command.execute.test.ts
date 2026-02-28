import test from 'node:test';
import assert from 'node:assert';
import { ContractRunner } from '../../../../foundation/src/testing/contract-runner';

test('Contract: pipe.command.execute.v1', async (t) => {
    const runner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.command.execute.v1.schema.json');

    await t.test('Validates a compliant payload with valid execution_authz', () => {
        const validExecution = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174010',
                producer: 'topic-orchestration',
                schema_version: '1.0.0'
            },
            data: {
                command_id: '550e8400-e29b-41d4-a716-446655440000',
                target_system: 'appfolio',
                action: 'apply_late_fee',
                parameters: {
                    tenant_id: 'uuid-123',
                    amount: 50.00
                },
                execution_authz: {
                    token: 'crypto-signed-token-XYZ',
                    approved_by: 'System-Auto',
                    risk_tier: 1
                }
            }
        };

        runner.assertValid(validExecution);
    });

    await t.test('Rejects payload missing execution_authz entirely', () => {
        const missingAuthz = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174010',
                producer: 'topic-orchestration',
                schema_version: '1.0.0'
            },
            data: {
                command_id: '550e8400-e29b-41d4-a716-446655440000',
                target_system: 'appfolio',
                action: 'apply_late_fee',
                parameters: {
                    tenant_id: 'uuid-123',
                    amount: 50.00
                }
            }
        };

        runner.assertInvalid(missingAuthz);
    });

    await t.test('Rejects payload with missing target_system', () => {
        const missingTarget = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174010',
                producer: 'topic-orchestration',
                schema_version: '1.0.0'
            },
            data: {
                command_id: '550e8400-e29b-41d4-a716-446655440000',
                action: 'apply_late_fee',
                parameters: {},
                execution_authz: {
                    token: 'crypto-signed-token-XYZ',
                    approved_by: 'System-Auto',
                    risk_tier: 1
                }
            }
        };

        runner.assertInvalid(missingTarget);
    });
});
