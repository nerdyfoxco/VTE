"use client";
export const dynamic = 'force-dynamic';

import { useEffect, useState } from 'react';
import axios from 'axios';
import { useRouter, useSearchParams } from 'next/navigation';

import { Suspense } from 'react';

function CallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [status, setStatus] = useState("Processing Google Login...");
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const handleCallback = async () => {
            const code = searchParams.get('code');
            if (!code) {
                setError("No Authorization Code found in URL.");
                return;
            }

            try {
                const token = localStorage.getItem('access_token');

                await axios.post('http://localhost:8000/api/v1/connect/gmail/callback',
                    { code },
                    { headers: { Authorization: `Bearer ${token}` } }
                );

                setStatus("Success! Gmail Connected. Redirecting...");
                setTimeout(() => router.push('/connect'), 1500);

            } catch (e: any) {
                console.error(e);
                setError("Connection Failed: " + (e.response?.data?.detail || e.message));
            }
        };

        handleCallback();
    }, [searchParams, router]);

    return (
        <div className="bg-white p-8 rounded shadow text-center">
            {error ? (
                <div className="text-red-500 font-bold">
                    ❌ Error: {error}
                    <div className="mt-4">
                        <button onClick={() => router.push('/connect')} className="text-blue-500 underline">Try Again</button>
                    </div>
                </div>
            ) : (
                <div className="text-green-600 font-medium">
                    <span className="animate-pulse">🔄</span> {status}
                </div>
            )}
        </div>
    );
}

export default function CallbackPage() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <Suspense fallback={<div>Loading Callback...</div>}>
                <CallbackContent />
            </Suspense>
        </div>
    );
}
