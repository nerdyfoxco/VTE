import { PrismaClient } from '@prisma/client';

export const revalidate = 0;

const prisma = new PrismaClient();

export default async function Page() {
    const policies = await prisma.policyVersion.findMany({
        include: { workspace: true },
        orderBy: { version: 'desc' }
    });

    return (
        <div className="space-y-8">
            <header className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-semibold tracking-tight">Policy Editor</h1>
                    <p className="text-zinc-400 mt-2 text-sm">Deterministic execution SOPs across the tenant fleet.</p>
                </div>
                <button className="px-4 py-2 bg-zinc-800 text-zinc-100 border border-zinc-700 text-sm font-medium rounded-md hover:bg-zinc-700 transition-colors">
                    Upload Custom DT
                </button>
            </header>

            <div className="grid grid-cols-2 gap-6">
                {policies.map(policy => (
                    <div key={policy.id} className="border border-zinc-800 rounded-xl bg-zinc-900/50 p-6 flex flex-col gap-4 shadow-sm hover:border-zinc-700 transition-colors">
                        <div className="flex justify-between items-start">
                            <div>
                                <h3 className="text-lg font-medium text-zinc-200">Arrears Ruleset</h3>
                                <p className="text-sm text-zinc-400 mt-1">Bound to: <span className="text-zinc-300 font-mono text-xs">{policy.workspace.id}</span></p>
                            </div>
                            {policy.isActive ? (
                                <span className="px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold tracking-wider">ACTIVE</span>
                            ) : (
                                <span className="px-2 py-1 rounded bg-zinc-800 text-zinc-500 border border-zinc-700 text-[10px] font-bold tracking-wider">ARCHIVED</span>
                            )}
                        </div>

                        <div className="grid grid-cols-2 gap-4 mt-2">
                            <div className="flex flex-col">
                                <span className="text-[10px] uppercase tracking-wider text-zinc-500 font-medium">Wait Time SLA</span>
                                <span className="text-sm font-medium text-zinc-300">{policy.globalWaitDays} Days</span>
                            </div>
                            <div className="flex flex-col">
                                <span className="text-[10px] uppercase tracking-wider text-zinc-500 font-medium">Contact Threshold</span>
                                <span className="text-sm font-medium text-zinc-300">Max {policy.contactThresholdMax}</span>
                            </div>
                        </div>

                        <div className="mt-2 p-3 bg-zinc-950 border border-zinc-800 rounded-md font-mono text-[11px] text-zinc-400 flex flex-col gap-1">
                            <div><span className="text-zinc-600">VERSION:</span> {policy.version}</div>
                            <div><span className="text-zinc-600">PID:</span> {policy.id}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
