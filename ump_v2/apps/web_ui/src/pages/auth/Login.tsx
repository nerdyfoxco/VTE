import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Mail, Lock, ShieldAlert, ArrowRight } from 'lucide-react';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            // Proxy maps /api to the Spine 8080 backend
            const response = await axios.post('/api/auth/signin', { email, password });

            // VTE 3.0 Fail-Closed: We expect an MFA Challenge, not a token.
            if (response.data.status === 'MFA_REQUIRED') {
                // Pass the challenge ID via router state so it can't be deep-linked easily
                navigate('/mfa', { state: { mfa_token_id: response.data.mfa_token_id, email } });
            } else {
                setError('Unexpected identity response state.');
            }
        } catch (err: any) {
            if (err.response && err.response.status === 401) {
                setError('Invalid credentials or account disabled.');
            } else {
                setError('VTE Engine Offline. Please try again later.');
            }
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 flex flex-col justify-center items-center p-4">
            <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-8 relative overflow-hidden">

                {/* Decorative Grid */}
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay pointer-events-none"></div>
                <div className="absolute top-0 right-0 -mr-16 -mt-16 w-48 h-48 rounded-full bg-blue-900/20 blur-3xl pointer-events-none"></div>

                <div className="flex items-center justify-center mb-8 relative z-10">
                    <div className="w-12 h-12 bg-blue-950/50 rounded-xl flex items-center justify-center border border-blue-500/30">
                        <Lock className="w-6 h-6 text-blue-400" />
                    </div>
                </div>

                <h2 className="text-3xl font-bold text-center text-white mb-2 relative z-10">VTE Identity</h2>
                <p className="text-slate-400 text-center mb-8 relative z-10">Sign in to the Operator OS</p>

                {error && (
                    <div className="mb-6 bg-red-950/50 border border-red-500/30 rounded-lg p-4 flex items-start text-red-400 text-sm relative z-10">
                        <ShieldAlert className="w-5 h-5 mr-3 flex-shrink-0" />
                        <p>{error}</p>
                    </div>
                )}

                <form onSubmit={handleLogin} className="space-y-6 relative z-10">
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">Email Address</label>
                        <div className="relative">
                            <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                                <Mail className="w-5 h-5 text-slate-500" />
                            </span>
                            <input
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-slate-950 border border-slate-700 rounded-lg py-3 pl-11 pr-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                placeholder="operator@company.com"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">Secure Password</label>
                        <div className="relative">
                            <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                                <Lock className="w-5 h-5 text-slate-500" />
                            </span>
                            <input
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full bg-slate-950 border border-slate-700 rounded-lg py-3 pl-11 pr-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                placeholder="••••••••••••"
                            />
                        </div>
                        <div className="flex justify-end mt-2">
                            <a href="#" className="text-xs text-blue-400 hover:text-blue-300 transition-colors">Forgot Master Password?</a>
                        </div>
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-3 rounded-lg transition-all flex items-center justify-center group"
                    >
                        Authenticate
                        <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                    </button>
                </form>

                <p className="mt-8 text-center text-sm text-slate-500 relative z-10">
                    VTE 3.0 Platform
                    <span className="mx-2">•</span>
                    <span className="mx-2">•</span>
                    <Link to="/signup" className="text-blue-400 hover:text-blue-300 transition-colors">Request Access</Link>
                    <span className="mx-2">•</span>
                    <a href="#" className="text-slate-500 hover:text-slate-400 transition-colors">Terms of Use</a>
                </p>
            </div>
        </div>
    );
}
