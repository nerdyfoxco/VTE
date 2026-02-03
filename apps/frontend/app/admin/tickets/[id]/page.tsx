'use client';

import { useEffect, useState, use } from 'react';
import { useRouter } from 'next/navigation'; // Correct import for App Router
// In App Router [id]/page.tsx, params are passed as props to the component.
// In Next.js 15, params is a Promise.

import { api } from '@/lib/api';

type Case = {
    id: string;
    title: string;
    description: string;
    status: string;
    tenant_id: string;
    created_at: string;
    balance: { amount: string; currency: string };
};

export default function TicketDetail({ params }: { params: Promise<{ id: string }> }) {
    const [c, setCase] = useState<Case | null>(null);
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState(false);
    const router = useRouter();
    const { id } = use(params);

    useEffect(() => {
        async function load() {
            try {
                const res = await api.get(`/api/cases/${id}`);
                setCase(res.data);
            } catch (err) {
                console.error("Load failed", err);
                // 404 handling? 
            } finally {
                setLoading(false);
            }
        }
        load();
    }, [id]);

    const updateStatus = async (newStatus: string) => {
        setUpdating(true);
        try {
            const res = await api.patch(`/api/cases/${id}/status`, { status: newStatus });
            setCase(res.data); // Update local state
        } catch (err: any) {
            alert("Update Failed: " + (err.response?.data?.detail || err.message));
        } finally {
            setUpdating(false);
        }
    };

    if (loading) return <div className="p-10 text-white">Loading...</div>;
    if (!c) return <div className="p-10 text-white">Case Not Found</div>;

    return (
        <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
            <button onClick={() => router.back()} className="mb-4 text-blue-400 hover:text-blue-200">← Back</button>

            <div className="bg-gray-800 rounded-xl p-8 border border-gray-700 shadow-2xl">
                <div className="flex justify-between items-start">
                    <div>
                        <span className="text-gray-500 font-mono text-sm">ID: {c.id}</span>
                        <h1 className="text-3xl font-bold mt-2 text-white">{c.title}</h1>
                        <p className="text-gray-400 mt-4 text-lg">{c.description || "No description provided."}</p>
                    </div>
                    <Badge status={c.status} />
                </div>

                <div className="mt-8 border-t border-gray-700 pt-8">
                    <h3 className="text-xl font-semibold mb-4 text-gray-300">Case Actions</h3>
                    <p className="text-sm text-gray-500 mb-4">Current Status: <span className="font-mono text-white">{c.status}</span></p>

                    <div className="flex gap-4">
                        {/* State Machine Transition Buttons */}
                        {/* Logic: We could check TRANSITIONS here, or just show all relevant ones and let backend reject */}

                        {c.status === 'OPEN' && (
                            <ActionButton label="Start Progress" onClick={() => updateStatus('IN_PROGRESS')} color="bg-blue-600 hover:bg-blue-500" disabled={updating} />
                        )}

                        {(c.status === 'OPEN' || c.status === 'IN_PROGRESS') && (
                            <ActionButton label="Resolve" onClick={() => updateStatus('RESOLVED')} color="bg-green-600 hover:bg-green-500" disabled={updating} />
                        )}

                        {/* Close? */}
                        {(c.status === 'OPEN' || c.status === 'IN_PROGRESS' || c.status === 'RESOLVED') && (
                            <ActionButton label="Close Case" onClick={() => updateStatus('CLOSED')} color="bg-gray-700 hover:bg-gray-600" disabled={updating} />
                        )}

                        {/* Re-Open? */}
                        {(c.status === 'CLOSED' || c.status === 'RESOLVED') && (
                            <ActionButton label="Re-Open" onClick={() => updateStatus('OPEN')} color="bg-yellow-600 hover:bg-yellow-500" disabled={updating} />
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function Badge({ status }: { status: string }) {
    const s = status.toUpperCase();
    let color = "bg-gray-600";
    if (s === 'OPEN') color = "bg-yellow-600";
    if (s === 'IN_PROGRESS') color = "bg-blue-600";
    if (s === 'RESOLVED') color = "bg-green-600";
    if (s === 'CLOSED' || s === 'URGENT') color = "bg-red-600";

    return <span className={`px-4 py-2 rounded-full text-sm font-bold text-white shadow-lg ${color}`}>{s}</span>;
}

function ActionButton({ label, onClick, color, disabled }: any) {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`px-6 py-3 rounded-lg font-semibold transition-all shadow-md active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed ${color} text-white`}
        >
            {label}
        </button>
    )
}
