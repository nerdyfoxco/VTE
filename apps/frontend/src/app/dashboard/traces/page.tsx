"use client";

import { useEffect, useState } from 'react';

// Explicit alignment with Prisma canonical execution traces
type ExecutionTrace = {
    id: string;
    tenantId: string;
    operatorId: string;
    state: 'SHADOW_VALIDATED' | 'LIVE_EXECUTED' | 'HALTED';
    contextSnapshot: any;
    createdAt: string;
};

export default function TraceDashboard() {
    const [traces, setTraces] = useState<ExecutionTrace[]>([]);
    const [loading, setLoading] = useState(true);

    // In Phase 3.5 we simulate fetching the exact /traces path.
    // We mock the API call in development since auth policies require live JWTs.
    useEffect(() => {
        // Simulated fetch aligning to the expected Express /traces endpoint payload
        setTimeout(() => {
            setTraces([
                {
                    id: 'trace-1111-2222',
                    tenantId: 'tenant-001',
                    operatorId: 'operator-admin',
                    state: 'SHADOW_VALIDATED',
                    contextSnapshot: {
                        originalRequest: { workflowName: 'ApproveLease', payload: { leaseId: 'L-555' } },
                        projectedEffects: [
                            { target: 'APPFOLIO_API', action: 'UPDATE_LEASE_STATUS', prediction: 'SUCCESS' },
                            { target: 'SENDGRID_API', action: 'EMAIL_TENANT', prediction: 'SUCCESS' }
                        ]
                    },
                    createdAt: new Date().toISOString()
                }
            ]);
            setLoading(false);
        }, 1000);
    }, []);

    return (
        <div className="p-8 max-w-7xl mx-auto font-sans">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Canonical Telemetry</h1>
                <p className="text-gray-500 mt-2">Human-in-the-loop visual audit log of the Shadow Execution Engine.</p>
            </div>

            {loading ? (
                <div className="flex animate-pulse space-x-4">
                    <div className="flex-1 space-y-4 py-1">
                        <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                        <div className="space-y-2">
                            <div className="h-4 bg-gray-200 rounded"></div>
                            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="grid gap-6">
                    {traces.map((trace) => (
                        <div key={trace.id} className="bg-white border shadow-sm rounded-xl p-6">
                            <div className="flex items-center justify-between border-b pb-4 mb-4">
                                <div className="flex items-center space-x-4">
                                    <span className="font-mono text-sm text-gray-500">{trace.id.split('-')[0]}</span>
                                    <span className="text-sm font-medium px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                                        {trace.contextSnapshot.originalRequest.workflowName}
                                    </span>
                                </div>
                                <div>
                                    {/* Explicit explicit SHADOW rendering */}
                                    <span className={`text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider ${trace.state === 'SHADOW_VALIDATED' ? 'bg-amber-100 text-amber-900 border border-amber-200' : 'bg-green-100 text-green-900'
                                        }`}>
                                        {trace.state.replace('_', ' ')}
                                    </span>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-8 text-sm">
                                <div>
                                    <h3 className="font-semibold text-gray-700 mb-2">Original Payload</h3>
                                    <pre className="bg-gray-50 p-3 rounded text-gray-600 overflow-x-auto">
                                        {JSON.stringify(trace.contextSnapshot.originalRequest.payload, null, 2)}
                                    </pre>
                                </div>
                                <div>
                                    <h3 className="font-semibold text-gray-700 mb-2">Projected Side Effects (Halted)</h3>
                                    <div className="space-y-2">
                                        {trace.contextSnapshot.projectedEffects.map((effect: any, idx: number) => (
                                            <div key={idx} className="bg-amber-50 border border-amber-100 p-3 rounded flex items-center justify-between">
                                                <span className="font-medium text-amber-900 text-xs tracking-wide">{effect.target}</span>
                                                <span className="text-amber-700">{effect.action}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            <div className="mt-6 pt-4 border-t text-xs text-gray-400 flex justify-between">
                                <span>Operator: {trace.operatorId}</span>
                                <span>{new Date(trace.createdAt).toLocaleString()}</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
