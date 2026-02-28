import { handlePolicyEvaluatePipe } from './src/pipes/evaluate-consumer';
import { ContractRunner } from '../../../foundation/src/testing/contract-runner';

const requestPayload = {
    meta: {
        event_id: '123e4567-e89b-12d3-a456-426614174000',
        timestamp_utc: new Date().toISOString(),
        correlation_id: 'corr-1010',
        producer: 'chapters/brain/topic-orchestration',
        schema_version: '1.0.0'
    },
    data: {
        policy_id: 'policy_eviction_threshold_v1',
        context: {
            tenant_ssn: '123-456-7890',
            months_delinquent: 5
        },
        requester: 'test-runner',
        dry_run: false
    }
};

const responsePayload = handlePolicyEvaluatePipe(requestPayload);
console.log("PAYLOAD_GENERATED:", JSON.stringify(responsePayload, null, 2));

const runner = new ContractRunner('foundation/contracts/pipes/schemas/pipe.policy.evaluated.v1.schema.json');
try {
    runner.assertValid(responsePayload);
    console.log("SCHEMA VALID!");
} catch (e: any) {
    console.log("AJV_SCHEMA_ERROR:\n", e.message);
}
