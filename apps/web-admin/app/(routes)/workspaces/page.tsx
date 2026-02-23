import { PrismaClient } from '@prisma/client';

export const revalidate = 0; // Dynamic route

const prisma = new PrismaClient();

export default async function Page() {
    const workspaces = await prisma.workspace.findMany({
        include: {
            _count: {
                select: { operators: true, policies: true }
            }
        },
        orderBy: { createdAt: 'desc' }
    });

    return (
        <div className="space-y-8">
            <header className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-semibold tracking-tight">Workspaces</h1>
                    <p className="text-zinc-400 mt-2 text-sm">Multi-tenant isolation boundaries enforced by the Spine.</p>
                </div>
                <button className="px-4 py-2 bg-zinc-50 text-zinc-950 text-sm font-medium rounded-md hover:bg-zinc-200 transition-colors">
                    New Workspace
                </button>
            </header>

            <div className="border border-zinc-800 rounded-xl overflow-hidden">
                <table className="w-full text-sm text-left">
                    <thead className="bg-zinc-900/50 text-zinc-400 border-b border-zinc-800">
                        <tr>
                            <th className="px-6 py-4 font-medium uppercase tracking-wider text-xs">Workspace Name</th>
                            <th className="px-6 py-4 font-medium uppercase tracking-wider text-xs">ID (Spine Key)</th>
                            <th className="px-6 py-4 font-medium uppercase tracking-wider text-xs">Operators</th>
                            <th className="px-6 py-4 font-medium uppercase tracking-wider text-xs">Policies</th>
                            <th className="px-6 py-4 font-medium uppercase tracking-wider text-xs">Status</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-zinc-800">
                        {workspaces.map((ws) => (
                            <tr key={ws.id} className="hover:bg-zinc-900/30 transition-colors">
                                <td className="px-6 py-4 font-medium text-zinc-200">{ws.name}</td>
                                <td className="px-6 py-4 text-zinc-500 font-mono text-xs">{ws.id}</td>
                                <td className="px-6 py-4 text-zinc-400">{ws._count.operators}</td>
                                <td className="px-6 py-4 text-zinc-400">{ws._count.policies}</td>
                                <td className="px-6 py-4">
                                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 shadow-sm shadow-emerald-500/20">
                                        Active
                                    </span>
                                </td>
                            </tr>
                        ))}
                        {workspaces.length === 0 && (
                            <tr>
                                <td colSpan={5} className="px-6 py-8 text-center text-zinc-500">No workspaces configured in SQLite.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
