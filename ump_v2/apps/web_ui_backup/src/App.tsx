import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShieldAlert, CheckCircle, Clock, RefreshCw } from 'lucide-react';

interface Trace {
    workspace_id: string;
    work_item_id: string;
    final_decision: string;
    action: string;
    trace_log: any;
    timestamp: string;
}

interface WorkItem {
    work_item_id: string;
    status: string;
    policy_outcome: string;
    timestamp: string;
}

const App: React.FC = () => {
    const [traces, setTraces] = useState<Trace[]>([]);
    const [workqueue, setWorkqueue] = useState<WorkItem[]>([]);
    const [syncing, setSyncing] = useState(false);

    const loadData = async () => {
        try {
            const [traceRes, workRes] = await Promise.all([
                axios.get('/api/traces'),
                axios.get('/api/workqueue')
            ]);
            setTraces(traceRes.data);
            setWorkqueue(workRes.data);
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const handleSync = async () => {
        setSyncing(true);
        try {
            await axios.post('/sync-gmail');
        } catch (e: any) {
            console.error("Sync error:", e.response?.data?.detail || e.message);
        } finally {
            await loadData();
            setSyncing(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-950 text-gray-200 p-8 font-sans">
            <div className="max-w-7xl mx-auto space-y-8">

                <div className="flex justify-between items-center border-b border-gray-800 pb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                            <ShieldAlert className="text-blue-500 w-8 h-8" />
                            VTE Operator Dashboard
                        </h1>
                        <p className="text-gray-400 mt-1">E2E Deterministic Runtime Trace Viewer</p>
                    </div>
                    <button
                        onClick={handleSync}
                        disabled={syncing}
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-md transition-colors"
                    >
                        <RefreshCw className={`w-4 h-4 ${syncing ? 'animate-spin' : ''}`} />
                        {syncing ? 'Syncing...' : 'Simulate Gmail Ingestion'}
                    </button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                    <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <Clock className="text-yellow-500 w-5 h-5" />
                            Workqueue (Pending Approval)
                        </h2>
                        <div className="space-y-3">
                            {workqueue.length === 0 ? (
                                <div className="text-gray-500 italic p-4 text-center">No items pending approval.</div>
                            ) : (
                                workqueue.map(item => (
                                    <div key={item.work_item_id} className="bg-gray-950 p-4 rounded border border-gray-800 flex justify-between items-center">
                                        <div>
                                            <div className="font-mono text-sm text-blue-400">{item.work_item_id}</div>
                                            <div className="text-xs text-gray-500 mt-1">{new Date(item.timestamp).toLocaleString()}</div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-sm font-bold text-yellow-500">{item.policy_outcome}</div>
                                            <div className="text-xs text-gray-400">{item.status}</div>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <CheckCircle className="text-green-500 w-5 h-5" />
                            Complete Execution Traces
                        </h2>
                        <div className="space-y-4">
                            {traces.length === 0 ? (
                                <div className="text-gray-500 italic p-4 text-center">No execution traces recorded.</div>
                            ) : (
                                traces.map((trace, i) => (
                                    <div key={i} className="bg-gray-950 p-4 rounded border border-gray-800">
                                        <div className="flex justify-between items-start mb-2">
                                            <div className="font-mono text-xs text-blue-400">{trace.work_item_id}</div>
                                            <div className="flex items-center gap-2">
                                                <span className={`px-2 py-0.5 text-xs rounded border ${trace.action === 'TERMINATE' ? 'bg-red-900/30 text-red-400 border-red-800' : 'bg-green-900/30 text-green-400 border-green-800'}`}>
                                                    {trace.action}
                                                </span>
                                                <span className="px-2 py-0.5 text-xs rounded border bg-gray-800 text-gray-300 border-gray-700">
                                                    {trace.final_decision}
                                                </span>
                                            </div>
                                        </div>

                                        <div className="bg-black/50 p-3 rounded text-xs font-mono text-gray-400 mt-2">
                                            <div className="text-white mb-1">Primary Reason: {trace.trace_log.primary}</div>
                                            <ul className="list-disc pl-4 space-y-1">
                                                {trace.trace_log.reasons.map((r: string, idx: number) => (
                                                    <li key={idx}>{r}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default App;
