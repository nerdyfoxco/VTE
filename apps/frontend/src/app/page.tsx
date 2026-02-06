"use client";
export const dynamic = 'force-dynamic';

import React, { useEffect, useState } from "react";
import { useRouter } from 'next/navigation';
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
    const [page, setPage] = useState(1);
    const [sortBy, setSortBy] = useState('priority');
    const [sortOrder, setSortOrder] = useState('asc');
    const [filterStatus, setFilterStatus] = useState('PENDING');
    const [filterPriority, setFilterPriority] = useState<string>('ALL');

    const pageSize = 5;

    const router = useRouter();

    useEffect(() => {
        const fetchQueue = async () => {
            setLoading(true);
            const token = localStorage.getItem('access_token');
            if (!token) {
                router.replace('/login');
                return;
            }

            try {
                const skip = (page - 1) * pageSize;
                let url = `http://localhost:8000/api/v1/queue?skip=${skip}&limit=${pageSize}&sort_by=${sortBy}&order=${sortOrder}&status=${filterStatus}`;

                if (filterPriority !== 'ALL') {
                    url += `&priority=${filterPriority}`;
                }

                const res = await axios.get(url, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setItems(res.data);
                setLoading(false);
            } catch (e: any) {
                console.error("Failed to fetch queue", e);
                if (e.response && e.response.status === 401) {
                    localStorage.removeItem('access_token');
                    router.replace('/login');
                } else {
                    setError(e.message);
                    setLoading(false);
                }
            }
        };
        fetchQueue();
    }, [router, page, sortBy, sortOrder, filterStatus, filterPriority]);

    const handleSort = (field: string) => {
        if (sortBy === field) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            setSortBy(field);
            setSortOrder('asc');
        }
        setPage(1); // Reset to page 1 on sort change
    };

    const SortIcon = ({ field }: { field: string }) => {
        if (sortBy !== field) return <span className="text-gray-300 ml-1">↕</span>;
        return <span className="text-indigo-600 ml-1">{sortOrder === 'asc' ? '↑' : '↓'}</span>;
    };

    if (loading) return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="text-gray-500">Loading VTE...</div>
        </div>
    );
    if (error) return <div className="p-8 text-red-600">Error: {error}</div>;

    return (
        <div className="min-h-screen bg-gray-100 py-10">
            <header className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
                <h1 className="text-3xl font-bold leading-tight text-gray-900">
                    Kevin's Work Day
                </h1>
                <p className="mt-2 text-sm text-gray-600">
                    Page <span className="font-bold text-indigo-600">{page}</span> | Showing {items.length} items
                </p>
                <div className="mt-4 flex flex-col sm:flex-row sm:items-center sm:justify-between bg-white p-4 rounded-lg shadow-sm">
                    {/* Filters */}
                    <div className="flex space-x-4 mb-4 sm:mb-0">
                        <select
                            value={filterStatus}
                            onChange={(e) => { setFilterStatus(e.target.value); setPage(1); }}
                            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                        >
                            <option value="PENDING">Status: Pending</option>
                            <option value="COMPLETED">Status: Completed</option>
                            <option value="ALL">Status: All</option>
                        </select>

                        <select
                            value={filterPriority}
                            onChange={(e) => { setFilterPriority(e.target.value); setPage(1); }}
                            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                        >
                            <option value="ALL">Priority: All</option>
                            <option value="1">Priority: P1</option>
                            <option value="2">Priority: P2</option>
                            <option value="3">Priority: P3</option>
                        </select>
                    </div>

                    {/* Sorting */}
                    <div className="flex space-x-4 text-sm items-center">
                        <span className="text-gray-500">Sort by:</span>
                        <button onClick={() => handleSort('priority')} className="font-medium hover:text-indigo-600 flex items-center">
                            Priority <SortIcon field="priority" />
                        </button>
                        <button onClick={() => handleSort('sla_deadline')} className="font-medium hover:text-indigo-600 flex items-center">
                            Due Date <SortIcon field="sla_deadline" />
                        </button>
                        <button onClick={() => handleSort('title')} className="font-medium hover:text-indigo-600 flex items-center">
                            Title <SortIcon field="title" />
                        </button>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="bg-white shadow overflow-hidden sm:rounded-md mb-6">
                    <ul role="list" className="divide-y divide-gray-200">
                        {items.length === 0 ? (
                            <li className="px-4 py-8 text-center text-gray-500">No items available.</li>
                        ) : items.map((item) => (
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
                                            id={`btn_process_${item.id}`}
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

                {/* Pagination Controls */}
                <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 shadow sm:rounded-md">
                    <div className="flex flex-1 justify-between sm:hidden">
                        <button
                            onClick={() => setPage(p => Math.max(1, p - 1))}
                            disabled={page === 1}
                            className={`relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium ${page === 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'}`}
                        >
                            Previous
                        </button>
                        <button
                            onClick={() => setPage(p => p + 1)}
                            disabled={items.length < pageSize}
                            className={`relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium ${items.length < pageSize ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'}`}
                        >
                            Next
                        </button>
                    </div>
                    <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                        <div>
                            <p className="text-sm text-gray-700">
                                Showing Page <span className="font-medium">{page}</span>
                            </p>
                        </div>
                        <div>
                            <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                                <button
                                    onClick={() => setPage(p => Math.max(1, p - 1))}
                                    disabled={page === 1}
                                    className={`relative inline-flex items-center rounded-l-md px-2 py-2 ring-1 ring-inset ring-gray-300 focus:z-20 focus:outline-offset-0 ${page === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-500 hover:bg-gray-50'}`}
                                >
                                    <span className="sr-only">Previous</span>
                                    <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                        <path fillRule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clipRule="evenodd" />
                                    </svg>
                                </button>
                                <button
                                    onClick={() => setPage(p => p + 1)}
                                    disabled={items.length < pageSize}
                                    className={`relative inline-flex items-center rounded-r-md px-2 py-2 ring-1 ring-inset ring-gray-300 focus:z-20 focus:outline-offset-0 ${items.length < pageSize ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-500 hover:bg-gray-50'}`}
                                >
                                    <span className="sr-only">Next</span>
                                    <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                        <path fillRule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clipRule="evenodd" />
                                    </svg>
                                </button>
                            </nav>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
