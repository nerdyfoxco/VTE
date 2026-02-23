import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
    console.log('[Seeder] Erasing existing dev.db state...');
    await prisma.promptVersion.deleteMany({});
    await prisma.approvalLedger.deleteMany({});
    await prisma.policyVersion.deleteMany({});
    await prisma.operator.deleteMany({});
    await prisma.workspace.deleteMany({});

    console.log('[Seeder] Injecting VTE Canonical Governance Foundations...');

    const ws = await prisma.workspace.create({
        data: {
            id: 'ws_vte_001',
            name: 'Vintloop Tenant Execution (Prod)',
            policies: {
                create: [
                    {
                        version: 'v1.0.4',
                        globalWaitDays: 5,
                        contactThresholdMax: 3,
                        isActive: true
                    },
                    {
                        version: 'v1.0.3-deprecated',
                        globalWaitDays: 7,
                        contactThresholdMax: 5,
                        isActive: false
                    }
                ]
            },
            operators: {
                create: [
                    { email: 'admin@vintloop.com', role: 'Compliance' },
                    { email: 'operator_1@vintloop.com', role: 'Operator' },
                ]
            }
        }
    });

    const ws2 = await prisma.workspace.create({
        data: {
            id: 'ws_vte_002',
            name: 'Acme Corp Real Estate',
            policies: {
                create: [
                    { version: 'v2.0.0-beta', globalWaitDays: 3, contactThresholdMax: 2, isActive: true }
                ]
            }
        }
    });

    console.log(`[Seeder] Successfully bound ${ws.id} and ${ws2.id} into the Control Plane.`);
}

main()
    .catch(e => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
