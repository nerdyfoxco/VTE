import React from 'react';
import { Server, Activity, Database, Shield, Settings2, Power, Terminal, ShieldAlert } from 'lucide-react';

export default function SuperAdminDashboard() {
    return (
        <div className="flex flex-col space-y-8 max-w-7xl mx-auto py-8 text-black px-6">
            <div className="flex flex-col border-b border-gray-200 pb-6">
                <div className="flex items-center gap-3">
                    <Shield className="h-8 w-8 text-indigo-600" />
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Super Admin Nexus</h1>
                        <p className="text-sm text-gray-500 mt-1">
                            System Health (APP-19) · Physical Runtime Controls · Telemetry Insights
                        </p>
                    </div>
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                <div className="flex flex-col p-6 rounded-xl border bg-white shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">Spine Status</span>
                        <Activity className="h-5 w-5 text-green-500" />
                    </div>
                    <div className="mt-4">
                        <span className="text-3xl font-bold">100%</span>
                        <p className="text-xs text-gray-500 mt-1">Zero Latency Detected</p>
                    </div>
                </div>
                <div className="flex flex-col p-6 rounded-xl border bg-white shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">Active Workers</span>
                        <Server className="h-5 w-5 text-blue-500" />
                    </div>
                    <div className="mt-4">
                        <span className="text-3xl font-bold">14</span>
                        <p className="text-xs text-gray-500 mt-1">across 3 nodes</p>
                    </div>
                </div>
                <div className="flex flex-col p-6 rounded-xl border bg-white shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">Prisma DB Sync</span>
                        <Database className="h-5 w-5 text-indigo-500" />
                    </div>
                    <div className="mt-4">
                        <span className="text-3xl font-bold">Stable</span>
                        <p className="text-xs text-gray-500 mt-1">last write 2s ago</p>
                    </div>
                </div>
                <div className="flex flex-col p-6 rounded-xl border bg-white shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-500 uppercase tracking-wider">Security Engine</span>
                        <ShieldAlert className="h-5 w-5 text-gray-400" />
                    </div>
                    <div className="mt-4">
                        <span className="text-3xl font-bold">Enabled</span>
                        <p className="text-xs text-gray-500 mt-1">Tenant isolation armed</p>
                    </div>
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <div className="rounded-xl border bg-white shadow-sm overflow-hidden flex flex-col">
                    <div className="bg-gray-50 px-6 py-4 border-b flex items-center justify-between">
                        <h3 className="font-semibold flex items-center gap-2"><Settings2 className="h-4 w-4" /> Global Feature Flags</h3>
                    </div>
                    <div className="p-6 flex flex-col space-y-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="font-medium">Force LLM Determinism Mode</p>
                                <p className="text-sm text-gray-500">Requires exactly matching reasons globally across operators.</p>
                            </div>
                            <div className="relative inline-block w-12 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" name="toggle" id="toggle1" defaultChecked className="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer" />
                                <label htmlFor="toggle1" className="toggle-label block overflow-hidden h-6 rounded-full bg-blue-500 cursor-pointer"></label>
                            </div>
                        </div>
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="font-medium">Halt All Operations Queues (Killswitch)</p>
                                <p className="text-sm text-gray-500">Instantly paralyzes all Data Plane interactions. Extreme danger.</p>
                            </div>
                            <div className="relative inline-block w-12 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" name="toggle" id="toggle2" className="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer" />
                                <label htmlFor="toggle2" className="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="rounded-xl border bg-gray-900 text-gray-100 shadow-sm overflow-hidden flex flex-col">
                    <div className="bg-gray-950 px-6 py-4 border-b border-gray-800 flex items-center justify-between">
                        <h3 className="font-semibold text-gray-200 flex items-center gap-2"><Terminal className="h-4 w-4" /> System Telemetry Log</h3>
                        <div className="flex gap-2">
                            <span className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse"></span>
                        </div>
                    </div>
                    <div className="p-6 font-mono text-xs flex flex-col space-y-2 h-64 overflow-y-auto">
                        <p><span className="text-gray-500">[12:44:01]</span> <span className="text-blue-400">INFO</span> [Spine] Evaluated Node WI-9021 → HOLD</p>
                        <p><span className="text-gray-500">[12:44:09]</span> <span className="text-green-400">OK</span> [DataPlane] Auth token strictly verified.</p>
                        <p><span className="text-gray-500">[12:45:12]</span> <span className="text-yellow-400">WARN</span> [Redis] Memory fluctuation detected: +4%</p>
                        <p><span className="text-gray-500">[12:45:15]</span> <span className="text-blue-400">INFO</span> [AppFolioAdapter] Session 901 initialized strictly.</p>
                        <p><span className="text-gray-500">[12:46:11]</span> <span className="text-green-400">OK</span> [Heart] Worker 3 reported backoff success organically.</p>
                    </div>
                </div>
            </div>

            <style dangerouslySetInnerHTML={{
                __html: `
                .toggle-checkbox:checked { right: 0; border-color: #3b82f6; }
                .toggle-checkbox:checked + .toggle-label { background-color: #3b82f6; }
                .toggle-checkbox { transition: all 0.2s ease-in-out; right: 24px; z-index: 10; border-color: #d1d5db; }
                .toggle-label { transition: all 0.2s ease-in-out; }
            `}} />
        </div>
    );
}
