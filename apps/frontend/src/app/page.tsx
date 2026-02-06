"use client";
export const dynamic = 'force-dynamic';

import React, { useEffect, useState } from "react";
import axios from 'axios';

// Contract: contracts/ux/unified_queue_truth_v1.json
interface QueueItem {
    id: string;
    title: string;
    priority: number;
    status: string;
    assigned_to?: string;
    sla_deadline: string;
}

export default function Dashboard() {
    const [items, setItems] = useState<QueueItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchQueue = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const res = await axios.get('http://localhost:8000/api/v1/queue', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setItems(res.data);
            } catch (e: any) {
                console.error("Failed to fetch queue", e);
                setError(e.message);
            } finally {
                setLoading(false);
            }
        };
        fetchQueue();
    }, []);

    if (loading) return <div className="p-8">Loading Kevin's Workspace...</div>;
    if (error) return <div className="p-8 text-red-600">Error: {error}</div>;

    return (
        <div className="min-h-screen bg-gray-100 py-10">
            <header className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
                <h1 className="text-3xl font-bold leading-tight text-gray-900">
                    Kevin's Work Day
                </h1>
                <p className="mt-2 text-sm text-gray-600">
                    You have <span className="font-bold text-indigo-600">{items.length}</span> active items in your queue.
                </p>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                    <ul role="list" className="divide-y divide-gray-200">
                        {items.map((item) => (
                            <li key={item.id}>
                                <div className="px-4 py-4 sm:px-6 hover:bg-gray-50 flex items-center justify-between">
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center justify-between">
                                            <p className="text-sm font-medium text-indigo-600 truncate">
                                                {item.title}
                                            </p>
                                            <div className="ml-2 flex-shrink-0 flex">
                                                <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                                                    ${item.priority === 1 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                                                    P{item.priority}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="mt-2 sm:flex sm:justify-between">
                                            <div className="sm:flex">
                                                <p className="flex items-center text-sm text-gray-500">
                                                    ID: {item.id}
                                                </p>
                                            </div>
                                            <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                                                <p>
                                                    Due: {new Date(item.sla_deadline).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="ml-5 flex-shrink-0">
                                        <button
                                            id="btn_export_audit" // Keeping ID for E2E
                                            className="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                                            onClick={() => alert(`Processing ${item.id}`)}
                                        >
                                            Process
                                        </button>
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
            </main>
        </div>
    );
}
