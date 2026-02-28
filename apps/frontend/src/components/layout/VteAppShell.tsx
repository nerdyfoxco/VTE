import React from 'react';
import VteSidebar from './VteSidebar';
import VteTopNav from './VteTopNav';

export default function VteAppShell({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="vte-app-shell flex min-h-screen bg-[#F5F5F7] font-sans antialiased text-[#1D1D1F]">
            <VteSidebar />
            <div className="flex flex-1 flex-col overflow-hidden">
                <VteTopNav />
                <main className="flex-1 overflow-y-auto px-4 py-6 md:px-8">
                    <div className="mx-auto max-w-7xl">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
