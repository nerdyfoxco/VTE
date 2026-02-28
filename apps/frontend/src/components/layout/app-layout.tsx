'use client';

import * as React from 'react';
import Link from 'next/link';
import { VteSidebar } from '@/components/layout/vte-sidebar';
import { VteTopNav } from '@/components/layout/vte-topnav';
import CookieConsent from '@/components/CookieConsent';

interface AppLayoutProps {
    children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
    return (
        <div className="vte-app-shell relative flex min-h-screen w-full bg-background overflow-hidden relative">
            <VteSidebar />
            <div className="flex flex-1 flex-col ml-[72px] h-screen overflow-hidden">
                <VteTopNav />
                <main className="flex-1 overflow-y-auto w-full max-w-none p-0 m-0 flex flex-col">
                    <div className="flex-1">
                        {children}
                    </div>
                    {/* App Footer */}
                    <footer className="w-full bg-white border-t border-gray-200 py-6 mt-10">
                        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
                            <div className="mb-4 md:mb-0">
                                &copy; {new Date().getFullYear()} VTE Enterprise. All rights reserved. Version 2.0.1
                            </div>
                            <div className="flex space-x-6">
                                <Link href="/privacy" className="hover:text-indigo-600 transition-colors">Privacy Policy</Link>
                                <Link href="/terms" className="hover:text-indigo-600 transition-colors">Terms of Service</Link>
                                <a href="mailto:support@vte-enterprise.com" className="hover:text-indigo-600 transition-colors">Support</a>
                            </div>
                        </div>
                    </footer>
                </main>
            </div>
            {/* Global Modals & Overlays */}
            <CookieConsent />
        </div>
    );
}
