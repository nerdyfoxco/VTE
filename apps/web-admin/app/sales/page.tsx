import React from 'react';
import { Target, TrendingUp, Building2, Phone, Mail, MoreHorizontal, Calendar, ArrowUpRight } from 'lucide-react';

export default function SalesConsolePage() {
    const pipelineData = {
        discovery: [
            { id: '1', company: 'Apex Property Management', contact: 'Jill C.', value: '$12,000 ARR', probability: '25%', lastContact: '2 days ago' },
            { id: '2', company: 'Summit Real Estate', contact: 'Marcus R.', value: '$18,500 ARR', probability: '30%', lastContact: '4 hrs ago' },
        ],
        proposal: [
            { id: '3', company: 'Vanguard Rentals', contact: 'David W.', value: '$45,000 ARR', probability: '60%', lastContact: '1 day ago' },
        ],
        negotiation: [
            { id: '4', company: 'Horizon Living', contact: 'Elena M.', value: '$32,000 ARR', probability: '85%', lastContact: '1 hr ago' },
            { id: '5', company: 'Pinnacle Estates', contact: 'Arthur B.', value: '$8,500 ARR', probability: '90%', lastContact: '3 days ago' },
        ],
    };

    return (
        <div className="flex flex-col space-y-8 max-w-[1600px] mx-auto py-8 text-black px-6">
            <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between border-b border-gray-200 pb-6 gap-4">
                <div className="flex items-center gap-3">
                    <Target className="h-8 w-8 text-emerald-600" />
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Revenue Pipeline</h1>
                        <p className="text-sm text-gray-500 mt-1">
                            Sales Console (SALES-SCR-01) · B2B Enterprise SaaS Deals
                        </p>
                    </div>
                </div>
                <div className="flex items-center gap-4">
                    <div className="flex flex-col items-end">
                        <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Total Pipeline ARR</span>
                        <span className="text-xl font-bold text-gray-900">$116,000</span>
                    </div>
                    <div className="h-10 w-px bg-gray-200"></div>
                    <button className="inline-flex items-center justify-center rounded-lg bg-gray-900 text-white px-4 py-2 text-sm font-medium hover:bg-gray-800 transition-colors">
                        Add Target Account
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-full pb-12">

                {/* Discovery Column */}
                <div className="flex flex-col space-y-4">
                    <div className="flex items-center justify-between bg-gray-50 border px-4 py-3 rounded-t-xl rounded-b-md shadow-sm border-b-2 border-b-gray-300">
                        <div className="flex items-center gap-2">
                            <span className="h-2 w-2 rounded-full bg-blue-400"></span>
                            <h3 className="font-semibold text-gray-700">Discovery</h3>
                            <span className="text-xs text-gray-400 bg-gray-200 px-2 py-0.5 rounded-full">{pipelineData.discovery.length}</span>
                        </div>
                        <span className="text-sm font-semibold text-gray-500">$30.5k</span>
                    </div>

                    <div className="flex flex-col space-y-3">
                        {pipelineData.discovery.map(deal => (
                            <div key={deal.id} className="bg-white border p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow group flex flex-col space-y-3">
                                <div className="flex justify-between items-start">
                                    <div className="flex flex-col gap-1">
                                        <h4 className="font-bold text-gray-900 leading-tight">{deal.company}</h4>
                                        <p className="text-xs text-gray-500 font-medium">{deal.contact}</p>
                                    </div>
                                    <button className="text-gray-300 hover:text-gray-600"><MoreHorizontal className="h-4 w-4" /></button>
                                </div>
                                <div className="flex justify-between items-end pt-2 border-t border-gray-100">
                                    <div className="flex flex-col">
                                        <span className="text-lg font-bold text-emerald-600">{deal.value}</span>
                                        <span className="text-[10px] text-gray-400 font-semibold">{deal.probability} PROBABILITY</span>
                                    </div>
                                    <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <button className="p-1.5 bg-gray-50 text-gray-600 rounded hover:bg-gray-200"><Phone className="h-3 w-3" /></button>
                                        <button className="p-1.5 bg-gray-50 text-gray-600 rounded hover:bg-gray-200"><Mail className="h-3 w-3" /></button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Proposal / Alignment Column */}
                <div className="flex flex-col space-y-4">
                    <div className="flex items-center justify-between bg-gray-50 border px-4 py-3 rounded-t-xl rounded-b-md shadow-sm border-b-2 border-b-amber-400">
                        <div className="flex items-center gap-2">
                            <span className="h-2 w-2 rounded-full bg-amber-400"></span>
                            <h3 className="font-semibold text-gray-700">Proposal / Alignment</h3>
                            <span className="text-xs text-gray-400 bg-gray-200 px-2 py-0.5 rounded-full">{pipelineData.proposal.length}</span>
                        </div>
                        <span className="text-sm font-semibold text-gray-500">$45k</span>
                    </div>

                    <div className="flex flex-col space-y-3">
                        {pipelineData.proposal.map(deal => (
                            <div key={deal.id} className="bg-white border p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow group flex flex-col space-y-3">
                                <div className="flex justify-between items-start">
                                    <div className="flex flex-col gap-1">
                                        <h4 className="font-bold text-gray-900 leading-tight">{deal.company}</h4>
                                        <p className="text-xs text-gray-500 font-medium">{deal.contact}</p>
                                    </div>
                                    <button className="text-gray-300 hover:text-gray-600"><MoreHorizontal className="h-4 w-4" /></button>
                                </div>
                                <div className="flex justify-between items-end pt-2 border-t border-gray-100">
                                    <div className="flex flex-col">
                                        <span className="text-lg font-bold text-emerald-600">{deal.value}</span>
                                        <span className="text-[10px] text-gray-400 font-semibold">{deal.probability} PROBABILITY</span>
                                    </div>
                                    <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <button className="p-1.5 bg-gray-50 text-gray-600 rounded hover:bg-gray-200"><Calendar className="h-3 w-3" /></button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Negotiation Column */}
                <div className="flex flex-col space-y-4">
                    <div className="flex items-center justify-between bg-gray-50 border px-4 py-3 rounded-t-xl rounded-b-md shadow-sm border-b-2 border-b-purple-500">
                        <div className="flex items-center gap-2">
                            <span className="h-2 w-2 rounded-full bg-purple-500"></span>
                            <h3 className="font-semibold text-gray-700">Negotiation / Commit</h3>
                            <span className="text-xs text-gray-400 bg-gray-200 px-2 py-0.5 rounded-full">{pipelineData.negotiation.length}</span>
                        </div>
                        <span className="text-sm font-semibold text-gray-500">$40.5k</span>
                    </div>

                    <div className="flex flex-col space-y-3">
                        {pipelineData.negotiation.map(deal => (
                            <div key={deal.id} className="bg-white border p-4 rounded-xl shadow-sm hover:border-purple-300 hover:shadow-md transition-colors group flex flex-col space-y-3">
                                <div className="flex justify-between items-start">
                                    <div className="flex flex-col gap-1">
                                        <h4 className="font-bold text-gray-900 leading-tight">{deal.company}</h4>
                                        <p className="text-xs text-gray-500 font-medium">{deal.contact}</p>
                                    </div>
                                    <ArrowUpRight className="h-4 w-4 text-emerald-500/50" />
                                </div>
                                <div className="flex justify-between items-end pt-2 border-t border-gray-100">
                                    <div className="flex flex-col">
                                        <span className="text-lg font-bold text-emerald-600">{deal.value}</span>
                                        <span className="text-[10px] text-gray-400 font-semibold">{deal.probability} PROBABILITY</span>
                                    </div>
                                    <span className="text-[10px] px-2 py-1 bg-green-50 text-green-700 font-semibold rounded-md border border-green-100">
                                        Verbal
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    );
}
