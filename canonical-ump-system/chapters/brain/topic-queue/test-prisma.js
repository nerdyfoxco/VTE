const { PrismaClient } = require('./node_modules/@prisma/client');
const prisma = new PrismaClient({ log: ['query', 'info', 'warn', 'error'] });

async function main() {
    try {
        console.log("Fetching QueueItems...");
        const items = await prisma.queueItem.findMany();
        console.log("SUCCESS:", items);
    } catch (e) {
        console.error("CRASH:", e);
    } finally {
        await prisma.$disconnect();
    }
}
main();
