'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

type Case = {
    id: string;
    title: string;
    status: string;
    tenant_id: string;
    created_at: string;
};

export default function AdminTickets() {
    const [role, setRole] = useState<string | null>(null);
    const [cases, setCases] = useState<Case[]>([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        // P3C: Bypassing local role check in favor of server-side validation & eventual session hook


        async function loadData() {
            try {
                const res = await api.get('/api/cases/');
                setCases(res.data);
            } catch (err) {
                console.error("Failed to load cases", err);
            } finally {
                setLoading(false);
            }
        }

        loadData();
    }, []);

    // ... (rest of layout, replacing table body)
    return (
        <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
            <header className="flex justify-between items-center mb-10 border-b border-gray-700 pb-4">
                <div>
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
                        VTE Operations Center
                    </h1>
                </div>
            </header>

            <main>
                <div className="bg-gray-800 rounded-xl overflow-hidden border border-gray-700 shadow-2xl">
                    <table className="w-full text-left">
                        <thead className="bg-gray-900/50 text-gray-400 uppercase text-xs">
                            <tr>
                                <th className="px-6 py-3">Status</th>
                                <th className="px-6 py-3">Title</th>
                                <th className="px-6 py-3">ID</th>
                                <th className="px-6 py-3">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-700">
                            {cases.map((c) => (
                                <tr key={c.id} className="hover:bg-gray-700/50 transition">
                                    <td className="px-6 py-4">
                                        <Badge status={c.status} />
                                    </td>
                                    <td className="px-6 py-4 font-medium text-white">{c.title}</td>
                                    <td className="px-6 py-4 font-mono text-sm text-gray-500">{c.id.slice(0, 8)}...</td>
                                    <td className="px-6 py-4">
                                        <button
                                            onClick={() => router.push(`/admin/tickets/${c.id}`)}
                                            className="text-blue-400 hover:text-blue-300 text-sm font-semibold"
                                        >
                                            View
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    );
}

function Badge({ status }: { status: string }) {
    const s = status.toUpperCase();
    if (s === 'URGENT' || s === 'CLOSED') return <span className="px-2 py-1 rounded text-xs font-bold bg-red-900/50 text-red-500 border border-red-500/30">{s}</span>;
    if (s === 'OPEN') return <span className="px-2 py-1 rounded text-xs font-bold bg-yellow-900/50 text-yellow-500 border border-yellow-500/30">{s}</span>;
    if (s === 'IN_PROGRESS') return <span className="px-2 py-1 rounded text-xs font-bold bg-blue-900/50 text-blue-500 border border-blue-500/30">{s}</span>;
    return <span className="px-2 py-1 rounded text-xs font-bold bg-green-900/50 text-green-500 border border-green-500/30">{s}</span>;
}
