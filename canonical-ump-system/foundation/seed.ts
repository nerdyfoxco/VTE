import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
    console.log("Seeding Canonical Default Tenant and Operator into PostgreSQL...");

    const tenant = await prisma.tenant.upsert({
        where: { id: '00000000-0000-0000-0000-000000000001' },
        update: {},
        create: {
            id: '00000000-0000-0000-0000-000000000001',
            name: 'VTE Default Operations Tenant',
            subscriptionTier: 'enterprise',
        }
    });

    console.log(`Ensured Tenant: ${tenant.name}`);

    // Create the Canonical Admin User Record
    const adminUser = await prisma.user.upsert({
        where: { email: 'admin@vintasoftware.com' },
        update: {},
        create: {
            id: '00000000-0000-0000-0000-000000000100',
            email: 'admin@vintasoftware.com',
            name: 'Vinta System Administrator'
        }
    });

    console.log(`Ensured Root User Identity: ${adminUser.email}`);

    const defaultOperator = await prisma.operator.upsert({
        where: { id: '00000000-0000-0000-0000-000000000009' },
        update: {},
        create: {
            id: '00000000-0000-0000-0000-000000000009',
            tenantId: tenant.id,
            userId: adminUser.id,
            role: 'admin',
        }
    });

    console.log(`Ensured Admin Operator Bound to Tenant.`);

    // Create the default VTE Workflow so ExecutionTraces have a foreign key to bind to
    const defaultWorkflow = await prisma.workflow.upsert({
        where: { id: '00000000-0000-0000-0000-000000000002' },
        update: {},
        create: {
            id: '00000000-0000-0000-0000-000000000002',
            tenantId: tenant.id,
            idempotencyKey: 'static-default-workflow-key',
            status: 'COMPLETED',
            payload: JSON.stringify({ description: "Default Canonical Workflow Mock" })
        }
    });

    console.log(`Ensured Default Workflow.`);

    // ==========================================
    // SEED KEVIN'S S.O.P. POLICY & RULES
    // ==========================================
    const kmPolicy = await prisma.policyVersion.upsert({
        where: { id: '00000000-0000-0000-0000-000000000010' },
        update: {},
        create: {
            id: '00000000-0000-0000-0000-000000000010',
            tenantId: tenant.id,
            name: "Kevin's Property Management SOPs",
            description: "Rules translating Kevin's daily duties into deterministic state transitions.",
            isActive: true,
            version: 1
        }
    });
    console.log(`Ensured Policy: ${kmPolicy.name}`);

    // Rule 1: Maintenance Delegation (Automated Hands Dispatch)
    await prisma.decisionRule.upsert({
        where: { id: '00000000-0000-0000-0000-000000000011' },
        update: {},
        create: {
            id: '00000000-0000-0000-0000-000000000011',
            policyId: kmPolicy.id,
            priority: 10,
            conditionType: 'EMAIL_CONTAINS',
            conditionValue: 'maintenance',
            action: 'DISPATCH_EMAIL',
            actionPayload: JSON.stringify({
                to: 'maintenance-vendor@example.com',
                template: 'Please review the attached maintenance request.'
            })
        }
    });

    // Rule 2: Exception Escalation (Fail-Closed HITL)
    await prisma.decisionRule.upsert({
        where: { id: '00000000-0000-0000-0000-000000000012' },
        update: {},
        create: {
            id: '00000000-0000-0000-0000-000000000012',
            policyId: kmPolicy.id,
            priority: 90,
            conditionType: 'EMAIL_CONTAINS',
            conditionValue: 'eviction',
            action: 'ESCALATE_HITL',
            actionPayload: JSON.stringify({
                reason: 'Eviction notices require strict manual Human-in-The-Loop review.'
            })
        }
    });
    console.log(`Ensured Kevin's Decision Rules mapped.`);

    console.log("Seeding complete. Execute `npx tsx seed.ts` to run.");
}

main()
    .catch(e => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
