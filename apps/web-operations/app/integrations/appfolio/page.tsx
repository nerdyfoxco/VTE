'use client';

import { useState, useEffect } from 'react';

export default function AppFolioIntegration() {
    const [state, setState] = useState({
        status: 'OFFLINE',
        message: 'Engine Offline. Press Start to boot the RPA pipeline.',
        otpCountdown: 0,
        actionPhase: 'NONE'
    });

    const fetchState = async () => {
        try {
            const res = await fetch('/api/appfolio/state');
            const data = await res.json();
            setState(data);
        } catch (e) { }
    };

    useEffect(() => {
        const interval = setInterval(fetchState, 1000);
        return () => clearInterval(interval);
    }, []);

    const sendAction = async (action: string, payload: any = null) => {
        await fetch('/api/appfolio/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action, payload })
        });
        fetchState();
    };

    const submitOTP = () => {
        const input = document.getElementById('otp_input') as HTMLInputElement;
        if (input && input.value) {
            sendAction('SUBMIT', input.value);
        }
    };

    return (
        <div className="p-8 max-w-4xl mx-auto mt-20">
            <div className="mb-8 border-b border-zinc-800 pb-4">
                <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">AppFolio Orchestration Engine</h1>
                <p className="text-zinc-400">Physical Headed Browser Data Extraction Pipeline</p>
            </div>

            <div className={`p-6 rounded-xl border mb-8 ${state.status === 'FAILED' || state.status === 'CRASHED' ? 'bg-red-500/10 border-red-500/20' : 'bg-zinc-900/50 border-zinc-800'}`}>
                <div className="text-xs uppercase tracking-widest text-zinc-500 font-semibold mb-2">System Status</div>
                <div className="text-xl font-medium text-emerald-400 mb-1">{state.status}</div>
                <div className="text-zinc-300">{state.message}</div>
            </div>

            <div className="space-y-4">
                {state.status === 'OFFLINE' && (
                    <button onClick={() => sendAction('START_PIPELINE')} className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-3 px-6 rounded-lg transition-colors border border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
                        Boot AppFolio Scraper
                    </button>
                )}

                {state.actionPhase === 'AVAILABILITY' && (
                    <div className="flex gap-4">
                        <button onClick={() => sendAction('YES')} className="bg-emerald-600 hover:bg-emerald-500 text-white py-2 px-4 rounded shadow-lg">Yes - Proceed</button>
                        <button onClick={() => sendAction('NO')} className="bg-rose-600 hover:bg-rose-500 text-white py-2 px-4 rounded shadow-lg">No - Try Again in 60 Mins</button>
                        <button onClick={() => sendAction('5_MINS')} className="bg-amber-600 hover:bg-amber-500 text-white py-2 px-4 rounded shadow-lg">In 5 Minutes</button>
                    </div>
                )}

                {state.actionPhase === 'CAPTCHA_CHECK' && (
                    <div className="flex gap-4">
                        <button onClick={() => sendAction('YES')} className="bg-emerald-600 hover:bg-emerald-500 text-white py-2 px-4 rounded shadow-lg">Yes - HITL is Online</button>
                        <button onClick={() => sendAction('NO')} className="bg-rose-600 hover:bg-rose-500 text-white py-2 px-4 rounded shadow-lg">No - Alert Admin</button>
                    </div>
                )}

                {(state.actionPhase === 'CAPTCHA_CONFIRM' || state.actionPhase === 'OTP_CONFIRM_MANUAL') && (
                    <button onClick={() => sendAction('CONFIRM')} className="bg-blue-600 hover:bg-blue-500 text-white font-medium py-3 px-6 rounded-lg shadow-lg">
                        Confirm I physically resolved it in browser
                    </button>
                )}

                {(state.actionPhase === 'OTP' || state.actionPhase === 'OTP_RETRY') && (
                    <div className="bg-zinc-900 border border-zinc-700 p-6 rounded-xl flex flex-col gap-4 max-w-sm">
                        <label className="text-zinc-300 font-medium">Enter 6-digit Code</label>
                        <input type="text" id="otp_input" className="bg-zinc-950 border border-zinc-700 rounded-lg p-3 text-2xl font-mono text-center tracking-[0.5em] text-white focus:outline-none focus:border-emerald-500" placeholder="------" />
                        <button onClick={submitOTP} className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-3 px-6 rounded-lg transition-colors shadow-lg">
                            Submit OTP
                        </button>

                        {state.actionPhase === 'OTP' && (
                            <div className="mt-4 pt-4 border-t border-zinc-800 text-center">
                                {state.otpCountdown > 0 ? (
                                    <div className="text-zinc-500 text-sm">No OTP Received? You can resend in {state.otpCountdown}s</div>
                                ) : (
                                    <button onClick={() => sendAction('RESEND')} className="text-rose-400 hover:text-rose-300 text-sm font-medium transition-colors">
                                        No OTP Received (Click to Resend)
                                    </button>
                                )}
                            </div>
                        )}
                    </div>
                )}

                {(state.status === 'DONE' || state.status === 'FAILED' || state.status === 'CRASHED') && (
                    <button onClick={() => sendAction('START_PIPELINE')} className="bg-zinc-800 hover:bg-zinc-700 text-white font-medium py-3 px-6 rounded-lg transition-colors border border-zinc-600">
                        Restart Flow
                    </button>
                )}
            </div>
        </div>
    );
}
