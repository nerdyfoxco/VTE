"use client";

import React from 'react';
import VteAppShell from '@/components/layout/VteAppShell';
import { CheckCircle2, XCircle, Clock } from 'lucide-react';

export default function ApprovalsPage() {
    return (
        <VteAppShell>
            <div className="flex flex-col space-y-6">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight">Governance Inbox (SC-0300)</h1>
                    <p className="text-sm text-gray-500 mt-1">Review ESCALATED or PENDING workflow transitions requiring Team Lead authorization.</p>
                </div>

                <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {/* Approval Card 1 */}
                    <div className="flex flex-col justify-between rounded-2xl border border-[#E5E5EA] bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
                        <div>
                            <div className="flex items-center justify-between mb-4">
                                <span className="inline-flex items-center rounded-full bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10">High Risk</span>
                                <span className="text-xs text-gray-400 font-mono">REQ-882</span>
                            </div>
                            <h3 className="text-md font-semibold text-gray-900 leading-tight mb-2">Notice to Quit Overwrite</h3>
                            <p className="text-sm text-gray-500 mb-4 line-clamp-3">
                                Operator OP-001 requested to force transition state to 10-DAY-NOTICE despite active tenant Promise to Pay record found in AppFolio.
                            </p>
                        </div>
                        <div className="flex items-center gap-2 mt-auto pt-4 border-t border-gray-100">
                            <button className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg bg-black px-3 py-2 text-xs font-semibold text-white hover:bg-gray-800 transition-colors">
                                <CheckCircle2 className="h-3.5 w-3.5" /> Approve
                            </button>
                            <button className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg border border-gray-200 bg-white px-3 py-2 text-xs font-semibold text-red-600 hover:bg-red-50 transition-colors">
                                <XCircle className="h-3.5 w-3.5" /> Reject
                            </button>
                        </div>
                    </div>

                    {/* Approval Card 2 */}
                    <div className="flex flex-col justify-between rounded-2xl border border-[#E5E5EA] bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
                        <div>
                            <div className="flex items-center justify-between mb-4">
                                <span className="inline-flex items-center rounded-full bg-amber-50 px-2 py-1 text-xs font-medium text-amber-700 ring-1 ring-inset ring-amber-600/10">Compliance Hold</span>
                                <span className="text-xs text-gray-400 font-mono">REQ-883</span>
                            </div>
                            <h3 className="text-md font-semibold text-gray-900 leading-tight mb-2">Outbound SMS Blocked</h3>
                            <p className="text-sm text-gray-500 mb-4 line-clamp-3">
                                Execution halted by Kidneys module. Trigger timestamp (9:05 PM) violates local timezone quiet hours compliance constraint.
                            </p>
                        </div>
                        <div className="flex items-center gap-2 mt-auto pt-4 border-t border-gray-100">
                            <button className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg bg-gray-100 px-3 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-200 transition-colors">
                                <Clock className="h-3.5 w-3.5" /> Reschedule AM
                            </button>
                            <button className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg border border-gray-200 bg-white px-3 py-2 text-xs font-semibold text-gray-900 hover:bg-gray-50 transition-colors">
                                Details
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </VteAppShell>
    );
}
