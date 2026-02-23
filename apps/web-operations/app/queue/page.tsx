"use client";

import { useState, useEffect } from "react";

// Mocking the structure of the incoming PipeEnvelopes from the Spine
interface WorkItem {
    id: string;
    location: string;
    unit: string;
    tenant: string;
    arrears: number;
    state: 'APPROVED' | 'HOLD' | 'STOP';
    reasonCode: string;
}

const INITIAL_QUEUE: WorkItem[] = [
    {
        id: "wi_001",
        location: "3118 N Bambrey St",
        unit: "Whole House",
        tenant: "Tonette Whitehead",
        arrears: 1030.00,
        state: "APPROVED",
        reasonCode: "CLEAR_TO_CONTACT"
    },
    {
        id: "wi_002",
        location: "1420 Walnut St",
        unit: "Unit 4B",
        tenant: "John Doe",
        arrears: 450.00,
        state: "STOP",
        reasonCode: "DNC_FLAG"
    },
    {
        id: "wi_003",
        location: "999 Market St",
        unit: "Apt 12",
        tenant: "Jane Smith",
        arrears: 2100.00,
        state: "HOLD",
        reasonCode: "JUDGMENT_BY_AGREEMENT"
    }
];

export default function Queue() {
    const [queue, setQueue] = useState<WorkItem[]>(INITIAL_QUEUE);
    const [selectedItem, setSelectedItem] = useState<WorkItem | null>(null);
    const [actionLog, setActionLog] = useState<string[]>([]);
    const [isExecuting, setIsExecuting] = useState(false);

    // Simulated ingestion polling
    useEffect(() => {
        const interval = setInterval(() => {
            // In a real environment, this would hit /api/pipe/poll
            console.log("Polling Spine for new WorkItems...");
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleExecute = async (item: WorkItem) => {
        setIsExecuting(true);
        // Simulate execution delay (Hands adapter)
        await new Promise(resolve => setTimeout(resolve, 800));

        setActionLog(prev => [`[${new Date().toLocaleTimeString()}] Executed PROTOCOL: ${item.reasonCode} mapped to ${item.tenant}`, ...prev]);
        setQueue(prev => prev.filter(i => i.id !== item.id));
        setIsExecuting(false);
        setSelectedItem(null);
    };

    const handleOverrideRequest = (item: WorkItem) => {
        setActionLog(prev => [`[${new Date().toLocaleTimeString()}] Requested L2 Supervisor Override for HOLD: ${item.id}`, ...prev]);
    };

    return (
        <div className="h-screen flex flex-col">
            <header className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-md px-8 py-4 sticky top-0 z-10 flex justify-between items-center">
                <div className="flex items-center gap-4">
                    <h1 className="text-xl font-medium tracking-tight">Active Work Queue</h1>
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-mono bg-zinc-800 text-zinc-300 border border-zinc-700">WORKSPACE: VTE-001</span>
                </div>
                <div className="flex gap-2 items-center">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-sm text-zinc-500 font-medium tracking-wide">SPINE SYNC: <span className="text-emerald-500">LIVE</span></span>
                </div>
            </header>

            <div className="flex-1 p-8 max-w-[1400px] w-full mx-auto animate-in fade-in duration-500 flex gap-8">

                <div className="flex-1 flex flex-col gap-6">
                    <div className="border border-zinc-800 rounded-lg overflow-hidden bg-zinc-900/40">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-zinc-900 text-zinc-500 border-b border-zinc-800">
                                <tr>
                                    <th className="px-6 py-3 font-medium uppercase tracking-wider text-[11px]">Location Identity</th>
                                    <th className="px-6 py-3 font-medium uppercase tracking-wider text-[11px]">Tenant</th>
                                    <th className="px-6 py-3 font-medium uppercase tracking-wider text-[11px] text-right">Ledger Arrears</th>
                                    <th className="px-6 py-3 font-medium uppercase tracking-wider text-[11px]">Compliance Engine</th>
                                    <th className="px-6 py-3 font-medium uppercase tracking-wider text-[11px] text-right">Execution Vector</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-zinc-800/50">
                                {queue.map((item) => {
                                    const isApproved = item.state === 'APPROVED';
                                    const isStop = item.state === 'STOP';
                                    const isHold = item.state === 'HOLD';

                                    return (
                                        <tr
                                            key={item.id}
                                            onClick={() => setSelectedItem(item)}
                                            className={`transition-colors cursor-pointer ${isStop ? 'bg-rose-950/10 hover:bg-rose-950/20 cursor-not-allowed' :
                                                isHold ? 'bg-amber-950/10 hover:bg-amber-950/20' :
                                                    'hover:bg-zinc-800/30 group'
                                                } ${selectedItem?.id === item.id ? 'ring-1 ring-inset ring-zinc-500 bg-zinc-800/20' : ''}`}
                                        >
                                            <td className={`px-6 py-4 ${isStop ? 'opacity-50' : ''}`}>
                                                <div className="font-medium text-zinc-200">{item.location}</div>
                                                <div className="text-zinc-500 text-xs mt-0.5">{item.unit}</div>
                                            </td>
                                            <td className={`px-6 py-4 text-zinc-300 ${isStop ? 'opacity-50' : ''}`}>{item.tenant}</td>
                                            <td className={`px-6 py-4 text-right font-mono ${isStop ? 'text-zinc-500 opacity-50' : isHold ? 'text-amber-400/80' : 'text-rose-400'}`}>
                                                ${item.arrears.toFixed(2)}
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex gap-2 items-center">
                                                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold border tracking-wider ${isApproved ? 'bg-zinc-800 text-emerald-400 border-emerald-500/20' :
                                                        isStop ? 'bg-rose-500/10 text-rose-500 border-rose-500/20' :
                                                            'bg-amber-500/10 text-amber-500 border-amber-500/20'
                                                        }`}>
                                                        {item.state}
                                                    </span>
                                                    <span className={`text-xs font-mono ${isApproved ? 'text-emerald-500/70 hidden' : isStop ? 'text-rose-500/70' : 'text-amber-500/70'}`}>
                                                        {item.reasonCode}
                                                    </span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 text-right">
                                                {isApproved && (
                                                    <button
                                                        onClick={(e) => { e.stopPropagation(); handleExecute(item); }}
                                                        disabled={isExecuting}
                                                        className="opacity-0 group-hover:opacity-100 transition-opacity px-4 py-1.5 bg-zinc-100 text-zinc-900 text-xs font-semibold rounded shadow-sm hover:bg-white disabled:opacity-50"
                                                    >
                                                        {isExecuting ? 'EXECUTING...' : 'EXECUTE'}
                                                    </button>
                                                )}
                                                {isStop && <span className="text-zinc-600 text-xs font-medium tracking-wide">LOCKED</span>}
                                                {isHold && (
                                                    <button
                                                        onClick={(e) => { e.stopPropagation(); handleOverrideRequest(item); }}
                                                        className="px-4 py-1.5 bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-semibold rounded hover:bg-amber-500/20 transition-colors"
                                                    >
                                                        REQUEST OVERRIDE
                                                    </button>
                                                )}
                                            </td>
                                        </tr>
                                    )
                                })}
                                {queue.length === 0 && (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-12 text-center text-zinc-500 text-sm">
                                            Queue is empty. Awaiting Spine ingress.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Execution Trace Sidebar */}
                <div className="w-80 flex flex-col gap-6">
                    <div className="border border-zinc-800 rounded-lg p-5 bg-zinc-900/40 flex flex-col gap-4">
                        <h3 className="text-sm font-medium tracking-wide text-zinc-400 uppercase">Execution Trace</h3>
                        <div className="flex flex-col gap-3 overflow-y-auto max-h-[60vh]">
                            {actionLog.map((log, i) => (
                                <div key={i} className="text-xs font-mono text-zinc-500 leading-relaxed border-l-2 border-zinc-800 pl-3">
                                    {log}
                                </div>
                            ))}
                            {actionLog.length === 0 && (
                                <div className="text-xs text-zinc-600 italic">No execution events recorded in this session.</div>
                            )}
                        </div>
                    </div>
                </div>

            </div>

            {/* Override Modal */}
            {selectedItem && selectedItem.state === 'HOLD' && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-in fade-in">
                    <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 max-w-md w-full shadow-2xl">
                        <div className="flex justify-between items-start mb-4">
                            <h2 className="text-lg font-medium text-amber-500 flex items-center gap-2">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                                Supervisor Override Required
                            </h2>
                            <button onClick={() => setSelectedItem(null)} className="text-zinc-500 hover:text-zinc-300">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                            </button>
                        </div>
                        <p className="text-sm text-zinc-400 mb-6 font-mono leading-relaxed px-3 py-3 bg-zinc-900 rounded mx-0">
                            WorkItem <span className="text-zinc-300">{selectedItem.id}</span> is locked due to Compliance Tag: <span className="text-amber-500 font-bold">{selectedItem.reasonCode}</span>. L2 Supervisor approval is mathematically required to proceed.
                        </p>
                        <div className="flex gap-3 justify-end mt-4">
                            <button onClick={() => setSelectedItem(null)} className="px-4 py-2 text-sm font-medium text-zinc-400 hover:text-zinc-50 transition-colors">Cancel</button>
                            <button onClick={() => { handleOverrideRequest(selectedItem); setSelectedItem(null); }} className="px-4 py-2 bg-amber-500 text-amber-950 text-sm font-semibold rounded hover:bg-amber-400 transition-colors">Request L2 Auth</button>
                        </div>
                    </div>
                </div>
            )}

        </div>
    )
}
