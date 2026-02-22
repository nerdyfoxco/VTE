"use client";
export const dynamic = 'force-dynamic';

import React, { useState } from "react";
import { api, EvidenceBundleDraft } from "../../lib/api";

export default function EvidencePage() {
    const [jsonInput, setJsonInput] = useState<string>(
        JSON.stringify(
            {
                normalization_schema: "plaid_txn_v1",
                items: [
                    {
                        source: "plaid",
                        type: "txn_row",
                        data: { amount: 500, merchant: "Acme Corp" },
                        sha256: "dummy_sha_of_data_" + Date.now()
                    }
                ]
            },
            null,
            2
        )
    );
    const [response, setResponse] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async () => {
        setError(null);
        setResponse(null);
        setIsLoading(true);
        try {
            const parsed = JSON.parse(jsonInput) as EvidenceBundleDraft;
            // Artificial delay to show the loading state (User Experience)
            await new Promise(r => setTimeout(r, 800));
            const res = await api.post("/evidence", parsed);
            setResponse(res.data);
        } catch (err: any) {
            setError(err.message || "Submission Failed");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="bg-white shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                    Submit Evidence Bundle
                </h3>
                <div className="mt-2 max-w-xl text-sm text-gray-500">
                    <p>
                        Raw JSON ingestion. Normalized schema is enforced by the backend canonicalizer.
                    </p>
                </div>
                <div className="mt-5">
                    <textarea
                        rows={12}
                        className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md font-mono bg-gray-50"
                        value={jsonInput}
                        onChange={(e) => setJsonInput(e.target.value)}
                    />
                </div>
                <div className="mt-3">
                    <button
                        onClick={handleSubmit}
                        type="button"
                        disabled={isLoading}
                        className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${isLoading ? "bg-blue-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
                            }`}
                    >
                        {isLoading ? (
                            <>
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Ingesting...
                            </>
                        ) : (
                            "Ingest Evidence"
                        )}
                    </button>
                </div>

                {error && (
                    <div className="mt-4 bg-red-50 border-l-4 border-red-400 p-4">
                        <div className="flex">
                            <div className="ml-3">
                                <p className="text-sm text-red-700">{error}</p>
                            </div>
                        </div>
                    </div>
                )}

                {response && (
                    <div className="mt-4 bg-green-50 border-l-4 border-green-400 p-4">
                        <div className="flex">
                            <div className="ml-3">
                                <h3 className="text-sm font-medium text-green-800">
                                    Success: Bundle Persisted
                                </h3>
                                <div className="mt-2 text-sm text-green-700">
                                    <p>Hash: {response.bundle_hash}</p>
                                    <pre className="mt-2 text-xs">{JSON.stringify(response, null, 2)}</pre>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
