import React from 'react';
import { CheckCircle, XCircle, FileQuestion, MoreHorizontal, ShieldAlert, ArrowRight } from 'lucide-react';

export default function ApprovalsInboxPage() {
    const mockApprovals = [
        { id: 'AUTH-L2-991', work_item: 'WI-9021', type: 'HOLD_OVERRIDE', tenant: 'Tonette N. Whitehead', reason: 'JBA Validation Required', age: '2h 15m', risk: 'High' },
        { id: 'AUTH-L2-992', work_item: 'WI-9025', type: 'WAIT_WAIVER', tenant: 'Marcus T. Vance', reason: 'Expedited Review', age: '45m', risk: 'Critical' },
        { id: 'AUTH-L2-993', work_item: 'WI-9028', type: 'COMPLIANCE_BYPASS', tenant: 'Sarah Jenkins', reason: 'Manual Document Verification', age: '1d 4h', risk: 'Medium' },
    ];

    return (
        <div className="flex flex-col space-y-6 max-w-7xl mx-auto py-8 px-6">
            <div className="flex items-center justify-between border-b pb-6">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-gray-900 flex items-center gap-3">
                        <ShieldAlert className="h-8 w-8 text-amber-500" />
                        Approvals Inbox
                    </h1>
                    <p className="text-sm text-gray-500 mt-2">
                        Control Plane (SC-0300) · L2 Supervisory Override Ledger
                    </p>
                </div>
            </div>

            <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="text-xs text-gray-500 uppercase bg-gray-50/80 border-b">
                            <tr>
                                <th className="px-6 py-4 font-medium tracking-wider">Auth Request ID</th>
                                <th className="px-6 py-4 font-medium tracking-wider">Context & Identity</th>
                                <th className="px-6 py-4 font-medium tracking-wider">Override Type</th>
                                <th className="px-6 py-4 font-medium tracking-wider">Exception Age</th>
                                <th className="px-6 py-4 text-right font-medium tracking-wider">Governance Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y">
                            {mockApprovals.map((item) => (
                                <tr key={item.id} className="hover:bg-gray-50/50 transition-colors group">
                                    <td className="px-6 py-4 font-mono font-semibold text-gray-900">
                                        {item.id}
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col gap-1">
                                            <span className="font-semibold text-gray-900">{item.tenant}</span>
                                            <span className="text-xs font-mono text-gray-500 flex items-center gap-1">
                                                {item.work_item}
                                                <ArrowRight className="h-3 w-3" />
                                                {item.reason}
                                            </span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wide uppercase ${item.type === 'WAIT_WAIVER' ? 'bg-purple-100 text-purple-700' :
                                                item.type === 'HOLD_OVERRIDE' ? 'bg-amber-100 text-amber-700' :
                                                    'bg-blue-100 text-blue-700'
                                            }`}>
                                            {item.type}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 font-medium text-gray-600">
                                        {item.age}
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <div className="flex items-center justify-end gap-2 opacity-80 group-hover:opacity-100 transition-opacity">
                                            <button className="inline-flex items-center justify-center rounded-md bg-green-50 text-green-700 px-3 py-1.5 text-xs font-semibold hover:bg-green-100 border border-green-200 transition-colors">
                                                <CheckCircle className="mr-1.5 h-3.5 w-3.5" /> Approve
                                            </button>
                                            <button className="inline-flex items-center justify-center rounded-md bg-red-50 text-red-700 px-3 py-1.5 text-xs font-semibold hover:bg-red-100 border border-red-200 transition-colors">
                                                <XCircle className="mr-1.5 h-3.5 w-3.5" /> Reject
                                            </button>
                                            <button className="inline-flex items-center justify-center rounded-md bg-gray-50 text-gray-700 px-3 py-1.5 text-xs font-semibold hover:bg-gray-100 border border-gray-200 transition-colors" title="Request RFI">
                                                <FileQuestion className="h-3.5 w-3.5" />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {mockApprovals.length === 0 && (
                        <div className="py-12 text-center text-gray-500 text-sm">
                            <CheckCircle className="mx-auto h-8 w-8 text-green-400 mb-3 opacity-50" />
                            No pending approvals in the inbox.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
