"use client";

import React, { useState } from "react";
import { api } from "../../lib/api";

export default function DecisionsPage() {
    const [decisionId, setDecisionId] = useState("");
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const fetchDecision = async () => {
        setError(null);
        setData(null);
        try {
            // Since we don't have a list endpoint yet, we fetch by ID or allow manual entry.
            // For MVP, if input is empty, maybe try a known one if we stored it?
            // Actually, backend needs a list endpoint.
            // For now, let's just fetch by ID. 
            if (!decisionId) throw new Error("Enter a Decision ID");

            const res = await api.get(`/decisions/${decisionId}`);
            setData(res.data);
        } catch (err: any) {
            setError(err.message || "Fetch Failed");
        }
    };

    return (
        <div className="bg-white shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                    Decision Chain Verification
                </h3>
                <div className="mt-2 max-w-xl text-sm text-gray-500">
                    <p>
                        Retrieve a Decision by ID to verify its cryptographic hash and previous link.
                    </p>
                </div>
                <div className="mt-5 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                    <div className="sm:col-span-4">
                        <label htmlFor="decision_id" className="block text-sm font-medium text-gray-700">
                            Decision UUID
                        </label>
                        <div className="mt-1">
                            <input
                                type="text"
                                name="decision_id"
                                id="decision_id"
                                className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                                placeholder="e.g. 550e8400-e29b-41d4-a716-446655440000"
                                value={decisionId}
                                onChange={(e) => setDecisionId(e.target.value)}
                            />
                        </div>
                    </div>
                    <div className="sm:col-span-2 flex items-end">
                        <button
                            onClick={fetchDecision}
                            type="button"
                            className="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                            Verify on Chain
                        </button>
                    </div>
                </div>

                {error && (
                    <div className="mt-4 text-red-600 text-sm">Error: {error}</div>
                )}

                {data && (
                    <div className="mt-6 border-t border-gray-100 pt-4">
                        <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
                            <div className="sm:col-span-1">
                                <dt className="text-sm font-medium text-gray-500">Decision Hash</dt>
                                <dd className="mt-1 text-sm text-gray-900 font-mono break-all">{data.decision_hash}</dd>
                            </div>
                            <div className="sm:col-span-1">
                                <dt className="text-sm font-medium text-gray-500">Previous Hash</dt>
                                <dd className="mt-1 text-sm text-gray-900 font-mono break-all">{data.previous_hash}</dd>
                            </div>
                            <div className="sm:col-span-1">
                                <dt className="text-sm font-medium text-gray-500">Timestamp</dt>
                                <dd className="mt-1 text-sm text-gray-900">{data.timestamp}</dd>
                            </div>
                            <div className="sm:col-span-1">
                                <dt className="text-sm font-medium text-gray-500">Outcome</dt>
                                <dd className="mt-1 text-sm font-bold text-green-600">{data.outcome}</dd>
                            </div>
                            <div className="sm:col-span-2">
                                <dt className="text-sm font-medium text-gray-500">Raw Data</dt>
                                <dd className="mt-1 text-xs text-gray-500 font-mono bg-gray-50 p-2 rounded">
                                    {JSON.stringify(data, null, 2)}
                                </dd>
                            </div>
                        </dl>
                    </div>
                )}
            </div>
        </div>
    );
}
