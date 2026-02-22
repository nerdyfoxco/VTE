import React from 'react';

/**
 * Phase 4 Operator UX: Decision Trace Viewer
 * Visualizes the deterministic DAG and rules evaluated by the Phase 2 Decision Table Compiler.
 */
export const DecisionTraceViewer: React.FC<{ traceId: string }> = ({ traceId }) => {
    return (
        <div className="p-4 border border-gray-700 bg-gray-800 text-gray-200 rounded-lg">
            <h3 className="text-lg font-semibold mb-2">Decision Trace: {traceId}</h3>
            <div className="bg-gray-900 p-3 rounded font-mono text-sm overflow-x-auto">
                <ul className="list-disc list-inside">
                    <li className="text-blue-400">ENG_RULE_01: `balance_owed` &gt; 0 [MATCH]</li>
                    <li className="text-blue-400">ENG_RULE_02: `status` == 'delinquent' [MATCH]</li>
                    <li className="text-red-400">COMPLIANCE_05: `jurisdiction` == 'NY' [FAIL -> STOP]</li>
                    <li className="text-yellow-400 mt-2">--&gt; Final Conclusion: TERMINATE</li>
                </ul>
            </div>
        </div>
    );
};
