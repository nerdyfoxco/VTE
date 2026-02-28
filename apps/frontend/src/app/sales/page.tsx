"use client";

import React from 'react';
import VteAppShell from '@/components/layout/VteAppShell';
import { ArrowRight, BarChart3, Users, DollarSign, Activity } from 'lucide-react';

const funnelMetrics = [
    { title: "Active Leads", value: "2,450", change: "+12.5%", icon: <Users className="h-5 w-5 text-gray-500" /> },
    { title: "Demos Scheduled", value: "184", change: "+4.2%", icon: <Activity className="h-5 w-5 text-gray-500" /> },
    { title: "Trials Initiated", value: "92", change: "+18.0%", icon: <BarChart3 className="h-5 w-5 text-blue-500" /> },
    { title: "Paid Active", value: "48", change: "+2.4%", icon: <DollarSign className="h-5 w-5 text-emerald-500" /> },
];

export default function SalesPage() {
    return (
        <VteAppShell>
            <div className="flex flex-col space-y-6">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight">Sales Pipeline (SALES-SCR-01)</h1>
                    <p className="text-sm text-gray-500 mt-1">Monitor cross-tenant funnel conversion and telemetry events without PII bleed.</p>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    {funnelMetrics.map((metric, idx) => (
                        <div key={idx} className="rounded-2xl border border-[#E5E5EA] bg-white p-6 shadow-sm">
                            <div className="flex items-center justify-between mb-4">
                                <span className="text-sm font-medium text-gray-500">{metric.title}</span>
                                <span className="rounded-full bg-gray-50 p-2">{metric.icon}</span>
                            </div>
                            <div className="flex items-baseline gap-2">
                                <span className="text-3xl font-bold tracking-tight text-gray-900">{metric.value}</span>
                                <span className="text-xs font-semibold text-emerald-600">{metric.change}</span>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Funnel Tracker */}
                <div className="rounded-2xl border border-[#E5E5EA] bg-white shadow-sm overflow-hidden mt-6">
                    <div className="border-b border-[#E5E5EA] bg-[#F5F5F7] px-6 py-4">
                        <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-widest">Live Progression Telemetry</h3>
                    </div>
                    <div className="p-6">
                        <div className="flex flex-col space-y-4">
                            {[
                                { tenant: "Greystar Management", stage: "PAID_ACTIVE", time: "2 min ago", stat: "Integration Value Delivered" },
                                { tenant: "Avalon Bay", stage: "ACTIVATION_ACHIEVED", time: "18 mins ago", stat: "12 Ledgers Parsed" },
                                { tenant: "Bozzuto Group", stage: "TRIAL_CREATED", time: "1 hour ago", stat: "Workspace Provisioned" },
                                { tenant: "Lincoln Property Co.", stage: "DEMO_SCHEDULED", time: "3 hours ago", stat: "Calendar Event Logged" },
                            ].map((log, i) => (
                                <div key={i} className="flex items-center justify-between border border-[#E5E5EA] rounded-xl p-4 hover:shadow-md transition-shadow">
                                    <div className="flex items-center gap-4">
                                        <div className="h-2 w-2 rounded-full bg-blue-500"></div>
                                        <div>
                                            <p className="text-sm font-semibold text-gray-900">{log.tenant}</p>
                                            <p className="text-xs font-mono text-gray-500">{log.stage}</p>
                                        </div>
                                    </div>
                                    <div className="hidden sm:flex flex-col text-right">
                                        <span className="text-xs font-medium text-gray-900">{log.stat}</span>
                                        <span className="text-xs text-gray-400">{log.time}</span>
                                    </div>
                                    <button className="text-sm font-semibold text-blue-600 hover:text-blue-800 transition-colors flex items-center gap-1">
                                        Telemetry <ArrowRight className="h-4 w-4" />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </VteAppShell>
    );
}
