import { DecisionEngine } from '../chapters/brain/topic-orchestration/src/rules';

async function main() {
    console.log("=== VTE DETERMINISTIC RULES EVALUATION V1 ===");

    // Fixed Tenant ID from Seed Script
    const TENANT_ID = '00000000-0000-0000-0000-000000000001';

    console.log("Test 1: Maintenance Delegation (Automated Path)");
    const maintenanceContext = {
        tenantId: TENANT_ID,
        workflowId: 'test-wf-1',
        currentOrgan: 'BRAIN',
        eventPayload: {
            sender: 'tenant@example.com',
            body: 'Hi, the sink is leaking and needs maintenance.'
        }
    };

    const result1 = await DecisionEngine.evaluateContext(maintenanceContext);
    console.log(`Action Result:`, result1);
    if (result1?.action === 'DISPATCH_EMAIL') {
        console.log("✅ Test 1 Passed: Evaluated maintenance correctly.");
    } else {
        console.error("❌ Test 1 Failed!");
    }

    console.log("\nTest 2: Eviction Notice (Fail-Closed HITL Path)");
    const evictionContext = {
        tenantId: TENANT_ID,
        workflowId: 'test-wf-2',
        currentOrgan: 'BRAIN',
        eventPayload: {
            sender: 'tenant@example.com',
            body: 'I received an eviction notice and need to talk to someone.'
        }
    };

    const result2 = await DecisionEngine.evaluateContext(evictionContext);
    console.log(`Action Result:`, result2);
    if (result2?.action === 'ESCALATE_HITL') {
        console.log("✅ Test 2 Passed: Evaluated eviction critical rule correctly.");
    } else {
        console.error("❌ Test 2 Failed!");
    }

    console.log("\nTest 3: Unknown Scenario (Fail-Closed Default)");
    const unknownContext = {
        tenantId: TENANT_ID,
        workflowId: 'test-wf-3',
        currentOrgan: 'BRAIN',
        eventPayload: {
            sender: 'bob@unknown.com',
            body: 'Can I rent a parking space?'
        }
    };

    const result3 = await DecisionEngine.evaluateContext(unknownContext);
    console.log(`Action Result:`, result3);
    if (result3?.action === 'ESCALATE_HITL') {
        console.log("✅ Test 3 Passed: Defaulted to Human-In-The-Loop on unknown.");
    } else {
        console.error("❌ Test 3 Failed!");
    }
}

main().catch(console.error);
