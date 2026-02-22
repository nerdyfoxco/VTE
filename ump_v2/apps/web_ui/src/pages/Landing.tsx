import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Lock, Activity, ArrowRight } from 'lucide-react';

const Landing: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-950 text-gray-200 font-sans flex flex-col">
            {/* Navigation Bar */}
            <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <ShieldCheck className="text-blue-500 w-8 h-8" />
                        <span className="text-xl font-bold tracking-tight text-white">VTE Platform</span>
                    </div>
                    <div className="flex items-center gap-4">
                        <Link to="/login" className="text-sm font-medium text-gray-400 hover:text-white transition-colors">
                            Operator Sign In
                        </Link>
                        <Link to="/signup" className="text-sm font-medium bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-md transition-colors shadow-lg shadow-blue-500/20">
                            Request Access
                        </Link>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <main className="flex-1 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 text-center py-20">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-900/30 border border-blue-800/50 text-blue-400 text-sm font-medium mb-8">
                    <span className="flex h-2 w-2 rounded-full bg-blue-500 animate-pulse"></span>
                    VTE 3.0 Production Build
                </div>

                <h1 className="text-5xl md:text-6xl font-extrabold text-white tracking-tight max-w-4xl leading-tight mb-6">
                    Deterministic Revenue Operations <br className="hidden md:block" /> for Property Management
                </h1>

                <p className="mt-4 text-xl text-gray-400 max-w-3xl mb-10 leading-relaxed">
                    <strong className="text-gray-200">Fail-Closed. Zero Ambiguity.</strong> Replace flawed human intuition with computationally verified debt collection and communication workflows.
                </p>

                <div className="flex flex-col sm:flex-row items-center gap-4">
                    <Link to="/signup" className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all hover:scale-105 shadow-xl shadow-blue-500/20 w-full sm:w-auto justify-center">
                        Request Operator Access <ArrowRight className="w-5 h-5" />
                    </Link>
                    <Link to="/login" className="flex items-center gap-2 bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 px-8 py-4 rounded-lg text-lg font-semibold transition-all w-full sm:w-auto justify-center">
                        Operator Sign In
                    </Link>
                </div>

                {/* Trust/Compliance Badges */}
                <div className="mt-20 pt-10 border-t border-gray-800 w-full max-w-4xl">
                    <p className="text-sm font-medium text-gray-500 uppercase tracking-widest mb-8">Architectural Constraints Enforced</p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="flex flex-col items-center p-4 rounded-xl bg-gray-900/40 border border-gray-800">
                            <ShieldCheck className="w-8 h-8 text-emerald-500 mb-3" />
                            <h3 className="text-gray-300 font-medium">Evidence Matrix Certified</h3>
                        </div>
                        <div className="flex flex-col items-center p-4 rounded-xl bg-gray-900/40 border border-gray-800">
                            <Lock className="w-8 h-8 text-purple-500 mb-3" />
                            <h3 className="text-gray-300 font-medium">SOC2 & PIA Compliant</h3>
                        </div>
                        <div className="flex flex-col items-center p-4 rounded-xl bg-gray-900/40 border border-gray-800">
                            <Activity className="w-8 h-8 text-blue-500 mb-3" />
                            <h3 className="text-gray-300 font-medium">Idempotency-Locked</h3>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="border-t border-gray-800 bg-gray-950 py-8">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div className="flex items-center gap-2 text-gray-500 text-sm">
                        <ShieldCheck className="w-4 h-4" /> © {new Date().getFullYear()} VTE Operating System
                    </div>
                    <div className="flex items-center gap-6 text-sm font-medium text-gray-500">
                        <a href="#" className="hover:text-gray-300 transition-colors">Privacy Impact Assessment (PIA)</a>
                        <a href="#" className="hover:text-gray-300 transition-colors">Business Continuity Plan (BCP)</a>
                        <a href="#" className="hover:text-gray-300 transition-colors">Terms of Service</a>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Landing;
