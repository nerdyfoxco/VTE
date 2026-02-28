"use client";

import React, { useState } from 'react';
import VteAppShell from '@/components/layout/VteAppShell';
import { ShieldAlert, Server, Activity, Power } from 'lucide-react';

export default function SuperAdminPage() {
    const [smsSwitch, setSmsSwitch] = useState(true);
    const [appFolioSync, setAppFolioSync] = useState(true);

    return (
        <VteAppShell>
            <div className="flex flex-col space-y-6">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-red-600 flex items-center gap-2">
                        <ShieldAlert className="h-6 w-6" /> Super Admin Center (APP-19)
                    </h1>
                    <p className="text-sm text-gray-500 mt-1">Platform Operations. Dual-Control authorization required for Mutative Acts.</p>
                </div>

                <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                    {/* Global Kill Switches */}
                    <div className="rounded-2xl border border-red-200 bg-red-50/30 p-6 shadow-sm">
                        <h3 className="text-lg font-semibold text-red-900 flex items-center gap-2 mb-6">
                            <Power className="h-5 w-5" /> Global Execution Toggles
                        </h3>

                        <div className="space-y-4">
                            <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-red-100 shadow-sm">
                                <div>
                                    <h4 className="text-sm font-semibold text-gray-900">Twilio SMS Egress Pipeline</h4>
                                    <p className="text-xs text-gray-500 mt-1">Instantly suspends all outgoing SMS messages entirely across all workspaces.</p>
                                </div>
                                <button
                                    onClick={() => setSmsSwitch(!smsSwitch)}
                                    className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2 ${smsSwitch ? 'bg-emerald-500' : 'bg-red-500'}`}
                                >
                                    <span className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${smsSwitch ? 'translate-x-5' : 'translate-x-0'}`} />
                                </button>
                            </div>

                            <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-red-100 shadow-sm">
                                <div>
                                    <h4 className="text-sm font-semibold text-gray-900">AppFolio Global Sync Ingress</h4>
                                    <p className="text-xs text-gray-500 mt-1">Halts RPA syncing. Active WorkQueues will freeze until unpaused.</p>
                                </div>
                                <button
                                    onClick={() => setAppFolioSync(!appFolioSync)}
                                    className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2 ${appFolioSync ? 'bg-emerald-500' : 'bg-red-500'}`}
                                >
                                    <span className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${appFolioSync ? 'translate-x-5' : 'translate-x-0'}`} />
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Infrastructure Health */}
                    <div className="rounded-2xl border border-[#E5E5EA] bg-white p-6 shadow-sm">
                        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-6">
                            <Activity className="h-5 w-5" /> Spine & Organs Telemetry
                        </h3>

                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-gray-600 flex items-center gap-2"><Server className="h-4 w-4" /> Queue DLQ (Dead Letter)</span>
                                <span className="text-sm font-mono font-semibold text-emerald-600">0 Items</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-1.5"><div className="bg-emerald-500 h-1.5 rounded-full w-[2%]"></div></div>

                            <div className="flex items-center justify-between pt-3">
                                <span className="text-sm text-gray-600 flex items-center gap-2"><Server className="h-4 w-4" /> DB Connection Pool</span>
                                <span className="text-sm font-mono font-semibold text-blue-600">42 / 100</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-1.5"><div className="bg-blue-500 h-1.5 rounded-full w-[42%]"></div></div>

                            <div className="flex items-center justify-between pt-3">
                                <span className="text-sm text-gray-600 flex items-center gap-2"><Server className="h-4 w-4" /> Redis Rate Limit Pressure</span>
                                <span className="text-sm font-mono font-semibold text-amber-500">76% Threshold</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-1.5"><div className="bg-amber-500 h-1.5 rounded-full w-[76%]"></div></div>
                        </div>
                    </div>
                </div>
            </div>
        </VteAppShell>
    );
}
