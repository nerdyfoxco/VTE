"use client";
export const dynamic = 'force-dynamic';

import { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import { API_URL } from '@/lib/api';

export default function ConnectPage() {
    const router = useRouter();
    const [uploading, setUploading] = useState(false);

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto space-y-8">

                {/* Header */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h1 className="text-2xl font-bold text-gray-900">Data Connections</h1>
                    <p className="mt-1 text-sm text-gray-500">
                        Connect your data sources to power the VTE Engine.
                    </p>
                </div>

                {/* 1. Email Connection */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-lg font-medium text-gray-900">1. Email Source</h2>
                    <p className="text-sm text-gray-500 mb-4">Connect Gmail to allow reading inbox for delinquency notifications.</p>

                    <button
                        onClick={async () => {
                            try {
                                const token = localStorage.getItem('access_token');
                                const res = await axios.get(`${API_URL}/connect/gmail/auth-url`, {
                                    headers: { Authorization: `Bearer ${token}` }
                                });
                                window.location.href = res.data.url;
                            } catch (e: any) {
                                alert("Failed to start Gmail Connect: " + (e.response?.data?.detail || e.message));
                            }
                        }}
                        className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                        <img className="h-5 w-5 mr-2" src="https://www.svgrepo.com/show/475656/google-color.svg" alt="" />
                        Connect Gmail Account (Real)
                    </button>
                    <span className="ml-3 text-sm text-yellow-600">⚠ Not Connected</span>
                </div>

                {/* 2. Delinquency Sheet */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-lg font-medium text-gray-900">2. Delinquency Report</h2>
                    <p className="text-sm text-gray-500 mb-4">Upload the latest 'Team A' Excel or CSV file.</p>

                    <div className="border-2 border-gray-300 border-dashed rounded-md p-6 flex justify-center items-center">
                        <div className="space-y-1 text-center">
                            <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                            <div className="flex text-sm text-gray-600">
                                <label className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                                    <span>Upload a file</span>
                                    <input id="file-upload" name="file-upload" type="file" className="sr-only" />
                                </label>
                                <p className="pl-1">or drag and drop</p>
                            </div>
                            <p className="text-xs text-gray-500">XLSX, CSV up to 10MB</p>
                        </div>
                    </div>
                </div>

                {/* 3. AppFolio Connection */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-lg font-medium text-gray-900">3. AppFolio Credentials</h2>
                    <p className="text-sm text-gray-500 mb-4">Enter credentials for the bot to check balances and take action.</p>

                    <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                        <div className="sm:col-span-3">
                            <label className="block text-sm font-medium text-gray-700">Username</label>
                            <input
                                id="af-username"
                                type="text"
                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                defaultValue="kevin@anchorrealtypa.com"
                            />
                        </div>
                        <div className="sm:col-span-3">
                            <label className="block text-sm font-medium text-gray-700">Password</label>
                            <input
                                id="af-password"
                                type="password"
                                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            />
                        </div>
                    </div>
                    <div className="mt-4">
                        <button
                            onClick={async () => {
                                try {
                                    const u = (document.getElementById('af-username') as HTMLInputElement).value;
                                    const p = (document.getElementById('af-password') as HTMLInputElement).value;
                                    if (!u || !p) { alert("Please enter both username and password"); return; }

                                    const token = localStorage.getItem('access_token');
                                    await axios.post(`${API_URL}/connect/appfolio/credentials`,
                                        { username: u, password: p },
                                        { headers: { Authorization: `Bearer ${token}` } }
                                    );
                                    alert("AppFolio Credentials Saved Successfully!");
                                } catch (e: any) {
                                    alert("Save Failed: " + (e.response?.data?.detail || e.message));
                                }
                            }}
                            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
                        >
                            Save Credentials
                        </button>
                    </div>
                </div>

                {/* Navigation */}
                <div className="flex justify-end">
                    <button
                        onClick={() => router.push('/dashboard')}
                        className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300"
                    >
                        Skip for Now &rarr;
                    </button>
                </div>

            </div>
        </div>
    );
}
