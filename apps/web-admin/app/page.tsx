import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export default async function Page() {
  const workspacesCount = await prisma.workspace.count();
  const policiesCount = await prisma.policyVersion.count();
  const activePoliciesCount = await prisma.policyVersion.count({ where: { isActive: true } });

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">System Authority</h1>
        <p className="text-zinc-400 mt-2 text-sm">Control Plane administration and multi-tenant governance.</p>
      </header>

      <div className="grid grid-cols-3 gap-4">
        <div className="p-6 rounded-xl border border-zinc-800 bg-zinc-900/50 flex flex-col gap-2">
          <span className="text-zinc-400 text-sm">Active Workspaces</span>
          <span className="text-3xl font-light tracking-tight">{workspacesCount}</span>
        </div>
        <div className="p-6 rounded-xl border border-zinc-800 bg-zinc-900/50 flex flex-col gap-2">
          <span className="text-zinc-400 text-sm">Policies (Active / Total)</span>
          <span className="text-3xl font-light tracking-tight">{activePoliciesCount} / {policiesCount}</span>
        </div>
        <div className="p-6 rounded-xl border border-zinc-800 bg-zinc-900/50 flex flex-col gap-2">
          <span className="text-zinc-400 text-sm">System Database</span>
          <div className="flex items-center gap-2 mt-1">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-sm font-medium text-emerald-500">Prisma (SQLite) Secured</span>
          </div>
        </div>
      </div>
    </div>
  )
}
