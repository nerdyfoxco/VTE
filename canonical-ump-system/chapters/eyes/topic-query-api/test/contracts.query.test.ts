import test from 'node:test';
import assert from 'node:assert';
import { ContractRunner } from '../../../../foundation/src/testing/contract-runner';

test('Contract: Bidirectional Query Pipes', async (t) => {
    const requestRunner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.query.request.v1.schema.json');
    const responseRunner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.query.response.v1.schema.json');

    await t.test('Validates compliant query request payload correctly', () => {
        const validRequest = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174010',
                producer: 'chapters/brain/topic-orchestration',
                schema_version: '1.0.0'
            },
            data: {
                query_id: '770e8400-e29b-41d4-a716-446655440111',
                domain: 'tenant_ledger',
                parameters: {
                    unit_id: 'unit_101'
                }
            }
        };

        requestRunner.assertValid(validRequest);
    });

    await t.test('Rejects request payload missing explicit domain boundaries', () => {
        const invalidRequest = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174010',
                producer: 'chapters/brain/topic-orchestration',
                schema_version: '1.0.0'
            },
            data: {
                query_id: '770e8400-e29b-41d4-a716-446655440111',
                parameters: {
                    unit_id: 'unit_101'
                }
            }
        };

        requestRunner.assertInvalid(invalidRequest);
    });

    await t.test('Validates compliant query response payload mapping lineage natively', () => {
        const validResponse = {
            meta: {
                event_id: '123e4567-e89b-12d3-a456-426614174000',
                timestamp_utc: new Date().toISOString(),
                correlation_id: '123e4567-e89b-12d3-a456-426614174010',
                producer: 'chapters/eyes/topic-query-api',
                schema_version: '1.0.0'
            },
            data: {
                original_query_id: '770e8400-e29b-41d4-a716-446655440111',
                status: 'found',
                payload: {
                    balance: 0,
                    delinquent: false
                },
                timestamp_fetched_utc: new Date().toISOString()
            }
        };

        responseRunner.assertValid(validResponse);
    });
});
