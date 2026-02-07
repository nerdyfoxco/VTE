"use client";
export const dynamic = 'force-dynamic';

import React, { useEffect, useState } from "react";
import { useRouter } from 'next/navigation';
import axios from 'axios';
import SkeletonLoader from '../components/SkeletonLoader';
import ErrorState from '../components/ErrorState';
import Breadcrumbs from '../components/Breadcrumbs';

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
    const [filterStatus, setFilterStatus] = useState('PENDING'); // Default to PENDING
    const [filterPriority, setFilterPriority] = useState<string>('ALL');
    const [searchQuery, setSearchQuery] = useState('');

    const pageSize = 5;

    const router = useRouter();

    // Gap 43: Content Density
    const [density, setDensity] = useState<'comfortable' | 'compact'>('comfortable');

    // Gap 44: Favorites
    const [favorites, setFavorites] = useState<string[]>([]);
    const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);

    // Gap 45: Bulk Actions
    const [selectedItems, setSelectedItems] = useState<string[]>([]);

    useEffect(() => {
        // Load settings from localStorage
        const savedDensity = localStorage.getItem('vte_density');
        if (savedDensity) setDensity(savedDensity as 'comfortable' | 'compact');

        const savedFavorites = localStorage.getItem('vte_favorites');
        if (savedFavorites) setFavorites(JSON.parse(savedFavorites));
    }, []);

    const toggleDensity = () => {
        const newDensity = density === 'comfortable' ? 'compact' : 'comfortable';
        setDensity(newDensity);
        localStorage.setItem('vte_density', newDensity);
    };

    const toggleFavorite = (id: string) => {
        let newFavs;
        if (favorites.includes(id)) {
            newFavs = favorites.filter(f => f !== id);
        } else {
            newFavs = [...favorites, id];
        }
        setFavorites(newFavs);
        localStorage.setItem('vte_favorites', JSON.stringify(newFavs));
    };

    const handleSelectRow = (id: string) => {
        if (selectedItems.includes(id)) {
            setSelectedItems(selectedItems.filter(i => i !== id));
        } else {
            setSelectedItems([...selectedItems, id]);
        }
    };

    const handleSelectAll = () => {
        if (selectedItems.length === items.length) {
            setSelectedItems([]);
        } else {
            setSelectedItems(items.map(i => i.id));
        }
    };
    useEffect(() => {
        fetchQueue();
    }, [router, page, sortBy, sortOrder, filterStatus, filterPriority, searchQuery]);

    const fetchQueue = async () => { // Move fetchQueue out or ensure it's accessible or just inline the retry logic to reload or re-trigger effect by state
        // Actually, better to just set a trigger state or define fetchQueue outside useEffect if possible, but inside component.
        // Let's refactor slightly to allow retry.
        setLoading(true);
        setError(null);
        // ... (logic)
    };

    // Wait, the previous useEffect defined fetchQueue INSIDE. I need to pull it out or use a "retry" counter state to trigger useEffect.

    // START REPLACEMENT STRATEGY
    // I will use a retry trigger state.
    const [retryTrigger, setRetryTrigger] = useState(0);

    useEffect(() => {
        const fetchQueue = async () => {
            setLoading(true);
            setError(null);
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

                if (searchQuery) {
                    url += `&search=${searchQuery}`;
                }

                const res = await axios.get(url, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                let fetchedItems = res.data;
                if (showFavoritesOnly) {
                    fetchedItems = fetchedItems.filter((i: any) => favorites.includes(i.id));
                }
                setItems(fetchedItems);
                setLoading(false);
            } catch (e: any) {
                console.error("Failed to fetch queue", e);
                if (e.response && e.response.status === 401) {
                    localStorage.removeItem('access_token');
                    router.replace('/login');
                } else {
                    setError(e.message || "An unexpected error occurred");
                    setLoading(false);
                }
            }
        };
        fetchQueue();
    }, [router, page, sortBy, sortOrder, filterStatus, filterPriority, searchQuery, retryTrigger]);

    // ...

    if (error) return (
        <ErrorState
            message={error}
            onRetry={() => setRetryTrigger(prev => prev + 1)}
        />
    );

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
        <div className="min-h-screen bg-gray-100 py-10">
            <header className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
                <h1 className="text-3xl font-bold leading-tight text-gray-900">
                    Kevin's Work Day
                </h1>
                <div className="h-4 w-48 bg-gray-200 rounded mt-2 animate-pulse"></div>

                <div className="mt-6 flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:items-center sm:justify-between bg-white p-4 rounded-lg shadow-sm animate-pulse">
                    <div className="h-10 bg-gray-200 rounded w-full sm:w-1/3"></div>
                    <div className="flex space-x-4">
                        <div className="h-10 bg-gray-200 rounded w-32"></div>
                        <div className="h-10 bg-gray-200 rounded w-32"></div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <SkeletonLoader />
            </main>
        </div>
    );
    if (error) return <div className="p-8 text-red-600">Error: {error}</div>;



    return (
        <div className="min-h-screen bg-gray-100 py-10">
            <header className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
                <div className="mb-4">
                    <Breadcrumbs items={[{ label: 'Home', href: '/' }, { label: 'Dashboard', href: '/dashboard' }, { label: "Kevin's Work Day" }]} />
                </div>
                <h1 className="text-3xl font-bold leading-tight text-gray-900">
                    Kevin's Work Day
                </h1>
                <p className="mt-2 text-sm text-gray-600">
                    Page <span className="font-bold text-indigo-600">{page}</span> | Showing {items.length} items
                </p>
                {/* Controls Area */}
                <div className="mt-6 flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:items-center sm:justify-between bg-white p-4 rounded-lg shadow-sm">
                    {/* Search */}
                    <div className="flex-1 max-w-lg mr-4">
                        <label htmlFor="search" className="sr-only">Search</label>
                        <div className="relative rounded-md shadow-sm">
                            <input
                                type="text"
                                name="search"
                                id="search"
                                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-4 sm:text-sm border-gray-300 rounded-md py-2 px-3"
                                placeholder="Search by Title..."
                                value={searchQuery}
                                onChange={(e) => { setSearchQuery(e.target.value); setPage(1); }}
                            />
                        </div>
                    </div>

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

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
                {/* Bulk Action Bar */}
                {selectedItems.length > 0 && (
                    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-indigo-900 text-white px-6 py-3 rounded-full shadow-lg z-50 flex items-center space-x-4 animate-fade-in-up">
                        <span className="font-medium">{selectedItems.length} items selected</span>
                        <div className="h-4 w-px bg-indigo-700"></div>
                        <button
                            onClick={() => alert(`Processing ${selectedItems.length} items`)}
                            className="hover:text-indigo-200 font-medium text-sm focus:outline-none"
                        >
                            Process Selected
                        </button>
                        <button
                            onClick={() => setSelectedItems([])}
                            className="text-indigo-400 hover:text-white text-sm focus:outline-none"
                        >
                            Clear
                        </button>
                    </div>
                )}

                {/* Filters & Controls */}
                <div className="mb-4 flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-4">
                    {/* Density Toggle */}
                    <button
                        id="btn-toggle-density"
                        onClick={() => toggleDensity()}
                        className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                        title="Toggle Density"
                    >
                        {density === 'comfortable' ? (
                            <>
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                                </svg>
                                Comfortable
                            </>
                        ) : (
                            <>
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                                </svg>
                                Compact
                            </>
                        )}
                    </button>

                    {/* Favorites Filter */}
                    <button
                        id="btn-favorites-filter"
                        onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
                        className={`inline-flex items-center px-3 py-2 border shadow-sm text-sm leading-4 font-medium rounded-md focus:outline-none ${showFavoritesOnly ? 'bg-indigo-50 border-indigo-500 text-indigo-700' : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'}`}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className={`h-5 w-5 mr-2 ${showFavoritesOnly ? 'text-yellow-400 fill-current' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                        </svg>
                        {showFavoritesOnly ? 'Favorites Only' : 'Show All'}
                    </button>
                </div>

                {/* Desktop View (Table) */}
                <div className="hidden sm:block bg-white shadow overflow-hidden sm:rounded-md mb-6">
                    <ul role="list" className="divide-y divide-gray-200">
                        {/* Table Header for Bulk Actions */}
                        {items.length > 0 && (
                            <li className="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center">
                                <div className="flex items-center h-5">
                                    <input
                                        id="select-all"
                                        name="select-all"
                                        type="checkbox"
                                        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                                        checked={items.length > 0 && selectedItems.length === items.length}
                                        onChange={handleSelectAll}
                                    />
                                </div>
                                <span className="ml-3 text-xs text-gray-500 uppercase tracking-wider font-medium">Select All</span>
                            </li>
                        )}

                        {items.length === 0 ? (
                            <div className="text-center py-12">
                                <svg
                                    className="mx-auto h-12 w-12 text-gray-400"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    aria-hidden="true"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                    />
                                </svg>
                                <h3 className="mt-2 text-sm font-medium text-gray-900">No items found</h3>
                                <p className="mt-1 text-sm text-gray-500">
                                    Try adjusting your search or filters to find what you're looking for.
                                </p>
                                <div className="mt-6">
                                    <button
                                        type="button"
                                        onClick={() => {
                                            setSearchQuery('');
                                            setFilterStatus('PENDING');
                                            setFilterPriority('ALL');
                                            setShowFavoritesOnly(false);
                                            setPage(1);
                                        }}
                                        className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                    >
                                        Clear Filters
                                    </button>
                                </div>
                            </div>
                        ) : items.map((item) => (
                            <li key={item.id}>
                                <div className={`px-4 ${density === 'compact' ? 'py-2' : 'py-4'} sm:px-6 hover:bg-gray-50 flex items-center justify-between transition-all duration-200`}>
                                    <div className="flex items-center flex-1 min-w-0">
                                        {/* Checkbox */}
                                        <div className="flex items-center h-5 mr-4">
                                            <input
                                                type="checkbox"
                                                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                                                checked={selectedItems.includes(item.id)}
                                                onChange={() => handleSelectRow(item.id)}
                                            />
                                        </div>

                                        {/* Star / Favorite */}
                                        <button
                                            onClick={() => toggleFavorite(item.id)}
                                            className="mr-3 focus:outline-none"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" className={`h-5 w-5 ${favorites.includes(item.id) ? 'text-yellow-400 fill-current' : 'text-gray-300 hover:text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                                            </svg>
                                        </button>

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
                                            <div className={`mt-2 sm:flex sm:justify-between ${density === 'compact' ? 'hidden' : ''}`}> {/* Hide details in compact mode */}
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
                                    </div>
                                    <div className="ml-5 flex-shrink-0">
                                        <button
                                            id={`btn_process_${item.id}`}
                                            className={`${density === 'compact' ? 'px-3 py-1 text-xs' : 'px-4 py-2 text-sm'} inline-flex items-center border border-transparent font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700`}
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
                {/* Mobile View (Cards) */}
                <div className="block sm:hidden space-y-4 mb-6">
                    {items.length === 0 ? (
                        <div className="text-center py-12 bg-white rounded-lg shadow">
                            {/* Mobile Empty State */}
                            <p className="text-gray-500">No items found.</p>
                            <button
                                onClick={() => { setSearchQuery(''); setFilterStatus('PENDING'); setFilterPriority('ALL'); setPage(1); }}
                                className="mt-4 text-indigo-600 font-medium"
                            >
                                Reset Filters
                            </button>
                        </div>
                    ) : items.map((item) => (
                        <div key={item.id} className="bg-white shadow rounded-lg p-4">
                            <div className="flex justify-between items-start">
                                <h3 className="text-lg font-medium text-indigo-600 truncate w-3/4">
                                    {item.title}
                                </h3>
                                <span className={`px-2 py-1 text-xs font-semibold rounded-full 
                                    ${item.priority === 1 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                                    P{item.priority}
                                </span>
                            </div>
                            <div className="mt-2 flex justify-between text-sm text-gray-500">
                                <span>ID: {item.id}</span>
                                <span>Due: {new Date(item.sla_deadline).toLocaleDateString()}</span>
                            </div>
                            <div className="mt-4">
                                <button
                                    className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                                    onClick={() => alert(`Processing ${item.id}`)}
                                >
                                    Process Item
                                </button>
                            </div>
                        </div>
                    ))}
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
