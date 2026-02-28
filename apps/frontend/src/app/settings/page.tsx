"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { QRCodeSVG } from 'qrcode.react';

export default function SettingsPage() {
    const [secret, setSecret] = useState<string | null>(null);
    const [qrUri, setQrUri] = useState<string | null>(null);
    const [code, setCode] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    // Using a simple state to determine if MFA is already set up could be done by fetching 
    // user profile, but for Phase 2 we will just provide the setup flow directly.

    const router = useRouter();

    const handleSetupMfa = async () => {
        setLoading(true);
        setError(null);
        setSuccess(null);
        try {
            const res = await api.post('/mfa/setup');
            setSecret(res.data.secret);
            setQrUri(res.data.uri);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to initialize MFA setup");
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyMfa = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            // Re-auth the device code to verify they set it up correctly
            const res = await api.post('/mfa/verify', { code });
            setSuccess("MFA has been successfully verified and enabled on your account.");
            // On success, the backend should mark it as confirmed="true"
            setSecret(null);
            setQrUri(null);
            setCode('');
        } catch (err: any) {
            setError(err.response?.data?.detail || "Invalid code. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="md:flex md:items-center md:justify-between mb-8">
                <div className="flex-1 min-w-0">
                    <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                        Account Settings
                    </h2>
                </div>
            </div>

            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                <div className="px-4 py-5 sm:px-6 border-b border-gray-200 flex justify-between items-center">
                    <div>
                        <h3 className="text-lg leading-6 font-medium text-gray-900">
                            Two-Factor Authentication (2FA)
                        </h3>
                        <p className="mt-1 max-w-2xl text-sm text-gray-500">
                            Secure your account using a Time-based One-Time Password (TOTP) application like Google Authenticator or Authy.
                        </p>
                    </div>
                </div>

                <div className="px-4 py-5 sm:p-6">
                    {error && (
                        <div className="mb-4 rounded-md bg-red-50 p-4">
                            <div className="flex">
                                <div className="ml-3">
                                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                                    <div className="mt-2 text-sm text-red-700">
                                        <p>{error}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {success && (
                        <div className="mb-4 rounded-md bg-green-50 p-4">
                            <div className="flex">
                                <div className="ml-3">
                                    <h3 className="text-sm font-medium text-green-800">Success</h3>
                                    <div className="mt-2 text-sm text-green-700">
                                        <p>{success}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {!qrUri && !success && (
                        <div>
                            <button
                                onClick={handleSetupMfa}
                                disabled={loading}
                                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                            >
                                Setup Authenticator App
                            </button>
                        </div>
                    )}

                    {qrUri && (
                        <div className="mt-5 border border-gray-200 rounded-md p-6 bg-gray-50">
                            <div className="md:flex md:items-start md:space-x-8">
                                <div className="flex-shrink-0 bg-white p-4 rounded-lg shadow-sm">
                                    <QRCodeSVG value={qrUri} size={200} />
                                </div>
                                <div className="mt-6 md:mt-0 flex-1">
                                    <h4 className="text-md font-medium text-gray-900">1. Scan the QR code</h4>
                                    <p className="mt-1 text-sm text-gray-500 mb-4">
                                        Open your authenticator app (e.g. Google Authenticator, Authy, 1Password) and scan the QR code to the left.
                                    </p>

                                    <h4 className="text-md font-medium text-gray-900 mt-4">Can't scan the code?</h4>
                                    <p className="mt-1 text-sm text-gray-500 mb-2">
                                        You can manually enter the secret key below into your app:
                                    </p>
                                    <code className="block p-2 bg-gray-100 rounded text-sm text-gray-800 font-mono tracking-wider break-all">
                                        {secret}
                                    </code>

                                    <h4 className="text-md font-medium text-gray-900 mt-8">2. Verify the code</h4>
                                    <p className="mt-1 text-sm text-gray-500 mb-4">
                                        Enter the 6-digit code generated by your app to verify the setup.
                                    </p>
                                    <form onSubmit={handleVerifyMfa} className="flex max-w-sm space-x-3">
                                        <input
                                            type="text"
                                            inputMode="numeric"
                                            pattern="[0-9]*"
                                            maxLength={6}
                                            value={code}
                                            onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                                            required
                                            placeholder="000000"
                                            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md py-2 px-3 text-center tracking-widest"
                                        />
                                        <button
                                            type="submit"
                                            disabled={loading || code.length !== 6}
                                            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                                        >
                                            Verify
                                        </button>
                                    </form>
                                    <div className="mt-4">
                                        <button
                                            onClick={() => { setQrUri(null); setSecret(null); setCode(''); }}
                                            className="text-sm text-gray-500 hover:text-gray-700 underline"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* System Information Section */}
            <div className="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
                <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                        System Information
                    </h3>
                    <p className="mt-1 max-w-2xl text-sm text-gray-500">
                        Application version and deployment environment details.
                    </p>
                </div>
                <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
                    <dl className="sm:divide-y sm:divide-gray-200">
                        <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt className="text-sm font-medium text-gray-500">Application Version</dt>
                            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">v2.0.1 (Enterprise Hardened)</dd>
                        </div>
                        <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt className="text-sm font-medium text-gray-500">Environment</dt>
                            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                    Production Active
                                </span>
                            </dd>
                        </div>
                        <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt className="text-sm font-medium text-gray-500">Database Engine</dt>
                            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">PostgreSQL 15 cluster</dd>
                        </div>
                    </dl>
                </div>
            </div>
        </div>
    );
}
