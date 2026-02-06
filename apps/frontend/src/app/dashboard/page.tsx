"use client";
import React, { useEffect, useState } from "react";
import { getQueueItems, QueueItem } from "@/lib/api";

export default function KevinWorkDayDashboard() {
    const [items, setItems] = useState<QueueItem[]>([]);

    useEffect(() => {
        getQueueItems().then(setItems);
    }, []);

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="flex justify-between mb-8">
                <h1 className="text-3xl font-bold leading-tight text-gray-900">
                    Kevin's Work Day (Unified Queue)
                </h1>
                <button
                    id="btn_export_audit"
                    className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                >
                    Export Audit
                </button>
            </div>

            <div className="flex flex-col">
                <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                        <div className="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Priority
                                        </th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Task
                                        </th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            SLA Deadline
                                        </th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Assigned To
                                        </th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Action
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {items.map((item) => (
                                        <tr key={item.id} className={new Date(item.sla_deadline) < new Date() ? "bg-red-50" : ""}>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${item.priority === 1 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                                                    }`}>
                                                    P{item.priority}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                {item.title}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {new Date(item.sla_deadline).toLocaleString()}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {item.assigned_to}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                                {item.title.includes("Approve Payment") ? (
                                                    <button
                                                        id="btn_approve_invoice"
                                                        className="text-green-600 hover:text-green-900 font-bold"
                                                    >
                                                        Approve
                                                    </button>
                                                ) : item.title.includes("User #") ? (
                                                    /* Potential match for btn_delete_user if logic required it, 
                                                       but keeping generic for review tasks */
                                                    <button className="text-indigo-600 hover:text-indigo-900">
                                                        Process
                                                    </button>
                                                ) : (
                                                    <button className="text-indigo-600 hover:text-indigo-900">
                                                        Process
                                                    </button>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
