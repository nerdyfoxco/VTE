import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Mail, Lock, User, Building2, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function Signup() {
    const [formData, setFormData] = useState({ email: '', password: '', full_name: '', tenant_id: '' });
    const [agreeAUP, setAgreeAUP] = useState(false);
    const [agreeSLA, setAgreeSLA] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState<{ totp_uri: string } | null>(null);
    const navigate = useNavigate();

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            const response = await axios.post('/api/auth/signup', formData);
            if (response.data.status === 'CREATED') {
                setSuccess({ totp_uri: response.data.totp_uri });
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Registration failed due to strict VTE constraints.');
        }
    };

    if (success) {
        return (
            <div className="min-h-screen bg-slate-950 flex flex-col justify-center items-center p-4">
                <div className="w-full max-w-md bg-slate-900 border border-green-900/50 rounded-xl shadow-2xl p-8 text-center relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-1 bg-green-500"></div>
                    <CheckCircle2 className="w-16 h-16 text-green-400 mx-auto mb-6" />
                    <h2 className="text-2xl font-bold text-white mb-2">Identity Created</h2>
                    <p className="text-slate-400 mb-6">Your Operator account has been minted. You must configure your Authenticator App immediately.</p>

                    <div className="bg-slate-950 rounded-lg p-4 mb-8 break-all border border-slate-800">
                        <p className="text-xs font-mono text-slate-500 text-left mb-2">TOTP Provisioning URI</p>
                        <code className="text-sm text-green-400">{success.totp_uri}</code>
                    </div>

                    <button onClick={() => navigate('/login')} className="w-full bg-slate-800 hover:bg-slate-700 text-white font-medium py-3 rounded-lg transition-all">
                        Proceed to Login
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 flex flex-col justify-center items-center p-4 pt-12 pb-12">
            <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-8 relative overflow-hidden">

                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay pointer-events-none"></div>
                <div className="absolute -bottom-16 -left-16 w-48 h-48 rounded-full bg-blue-900/20 blur-3xl pointer-events-none"></div>

                <h2 className="text-3xl font-bold text-center text-white mb-2">Request Access</h2>
                <p className="text-slate-400 text-center mb-8">Provision a VTE 3.0 Identity</p>

                {error && (
                    <div className="mb-6 bg-red-950/50 border border-red-500/30 rounded-lg p-4 flex items-start text-red-400 text-sm">
                        <ShieldAlert className="w-5 h-5 mr-3 flex-shrink-0" />
                        <p>{error}</p>
                    </div>
                )}

                <form onSubmit={handleSignup} className="space-y-5 relative z-10">
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">Operator Name</label>
                        <div className="relative">
                            <span className="absolute inset-y-0 left-0 flex items-center pl-3"><User className="w-5 h-5 text-slate-500" /></span>
                            <input type="text" required value={formData.full_name} onChange={(e) => setFormData({ ...formData, full_name: e.target.value })} className="w-full bg-slate-950 border border-slate-700 rounded-lg py-3 pl-11 pr-4 text-white focus:ring-2 focus:ring-blue-500 transition-all" placeholder="Operator Name" />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">Email Address</label>
                        <div className="relative">
                            <span className="absolute inset-y-0 left-0 flex items-center pl-3"><Mail className="w-5 h-5 text-slate-500" /></span>
                            <input type="email" required value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} className="w-full bg-slate-950 border border-slate-700 rounded-lg py-3 pl-11 pr-4 text-white focus:ring-2 focus:ring-blue-500 transition-all" placeholder="operator@company.com" />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">Tenant ID (Workspace)</label>
                        <div className="relative">
                            <span className="absolute inset-y-0 left-0 flex items-center pl-3"><Building2 className="w-5 h-5 text-slate-500" /></span>
                            <input type="text" required value={formData.tenant_id} onChange={(e) => setFormData({ ...formData, tenant_id: e.target.value })} className="w-full bg-slate-950 border border-slate-700 rounded-lg py-3 pl-11 pr-4 text-white focus:ring-2 focus:ring-blue-500 transition-all" placeholder="tnt_workspace_id" />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">Master Password (Min 12 Chars)</label>
                        <div className="relative">
                            <span className="absolute inset-y-0 left-0 flex items-center pl-3"><Lock className="w-5 h-5 text-slate-500" /></span>
                            <input type="password" required value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} className="w-full bg-slate-950 border border-slate-700 rounded-lg py-3 pl-11 pr-4 text-white focus:ring-2 focus:ring-blue-500 transition-all" placeholder="••••••••••••" />
                        </div>
                    </div>

                    <div className="space-y-3 pt-2">
                        <label className="flex items-start gap-3 cursor-pointer">
                            <input type="checkbox" required checked={agreeAUP} onChange={(e) => setAgreeAUP(e.target.checked)} className="mt-1 w-4 h-4 rounded border-slate-700 bg-slate-950 text-blue-600 focus:ring-blue-500 focus:ring-offset-slate-900" />
                            <span className="text-xs text-slate-400">I acknowledge that I am operating a fail-closed financial system. I will review all high-risk actions.</span>
                        </label>
                        <label className="flex items-start gap-3 cursor-pointer">
                            <input type="checkbox" required checked={agreeSLA} onChange={(e) => setAgreeSLA(e.target.checked)} className="mt-1 w-4 h-4 rounded border-slate-700 bg-slate-950 text-blue-600 focus:ring-blue-500 focus:ring-offset-slate-900" />
                            <span className="text-xs text-slate-400">I agree to the VTE Software Licensing and Data Processing Agreement.</span>
                        </label>
                    </div>

                    <button type="submit" disabled={!agreeAUP || !agreeSLA} className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-blue-900/50 disabled:text-blue-500/50 disabled:cursor-not-allowed text-white font-medium py-3 rounded-lg transition-all mt-4">
                        Provision Identity
                    </button>
                </form>

                <p className="mt-8 text-center text-sm text-slate-500 relative z-10">
                    <Link to="/login" className="text-slate-400 hover:text-white transition-colors">Cancel / Back to Login</Link>
                </p>
            </div>
        </div>
    );
}
