import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ShieldAlert, ShieldCheck, ArrowRight } from 'lucide-react';

export default function MFAChallenge() {
    const [totpCode, setTotpCode] = useState('');
    const [error, setError] = useState('');
    const location = useLocation();
    const navigate = useNavigate();

    // Protect route strictly: Must have valid MFA State from a successful Login call
    useEffect(() => {
        if (!location.state || !location.state.mfa_token_id) {
            navigate('/login', { replace: true });
        }
    }, [location, navigate]);

    const mfaState = location.state as { mfa_token_id: string, email: string } | null;

    const handleVerify = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!mfaState || totpCode.length !== 6) return;
        setError('');

        try {
            const response = await axios.post('/api/auth/mfa/verify', {
                mfa_token_id: mfaState.mfa_token_id,
                totp_code: totpCode
            });

            if (response.data.status === 'AUTHENTICATED') {
                // Persist session locally and navigate to secure dashboard
                localStorage.setItem('vte_session', response.data.session_token);
                navigate('/', { replace: true });
            }
        } catch (err: any) {
            if (err.response && err.response.status === 401) {
                setError('Invalid or expired authentication code.');
            } else {
                setError('Engine verification failed.');
            }
        }
    };

    if (!mfaState) return null; // Prevent flash before redirect

    return (
        <div className="min-h-screen bg-slate-950 flex flex-col justify-center items-center p-4">
            <div className="w-full max-w-sm bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-8 relative overflow-hidden">
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay pointer-events-none"></div>
                <div className="absolute top-0 right-0 w-full h-1 bg-blue-500"></div>

                <div className="flex justify-center mb-6">
                    <div className="bg-blue-900/30 p-4 rounded-full border border-blue-500/20">
                        <ShieldCheck className="w-10 h-10 text-blue-400" />
                    </div>
                </div>

                <h2 className="text-2xl font-bold text-center text-white mb-2 relative z-10">MFA Required</h2>
                <p className="text-slate-400 text-center mb-8 text-sm relative z-10">
                    Enter the 6-digit code from your authenticator app for <br /><span className="text-slate-300 font-medium">{mfaState.email}</span>
                </p>

                {error && (
                    <div className="mb-6 bg-red-950/50 border border-red-500/30 rounded-lg p-3 flex items-start text-red-400 text-sm relative z-10">
                        <ShieldAlert className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                        <p>{error}</p>
                    </div>
                )}

                <form onSubmit={handleVerify} className="space-y-6 relative z-10">
                    <div>
                        <input
                            type="text"
                            maxLength={6}
                            required
                            value={totpCode}
                            onChange={(e) => setTotpCode(e.target.value.replace(/[^0-9]/g, ''))} // Numeric only
                            className="w-full bg-slate-950 border border-slate-700 rounded-lg py-4 px-4 text-center text-2xl tracking-[0.5em] font-mono text-white placeholder-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-bold"
                            placeholder="000000"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={totpCode.length !== 6}
                        className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-medium py-3 rounded-lg transition-all flex items-center justify-center group"
                    >
                        Verify Identity
                        <ArrowRight className="w-5 h-5 ml-2 transition-transform" />
                    </button>
                </form>
            </div>
        </div>
    );
}
