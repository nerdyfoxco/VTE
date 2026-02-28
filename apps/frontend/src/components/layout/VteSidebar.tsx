import React from 'react';
import Link from 'next/link';
import { Home, CheckSquare, Settings, Users, ArrowRightLeft, LayoutDashboard } from 'lucide-react';

export default function VteSidebar() {
    const [isHovered, setIsHovered] = React.useState(false);

    return (
        <aside
            className="hidden md:flex flex-col w-64 border-r border-[#E5E5EA] bg-[#F5F5F7] min-h-screen text-[#1D1D1F] transition-all duration-300"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            <div className="flex items-center justify-between h-16 px-6 border-b border-[#E5E5EA] bg-white">
                <span className="text-sm font-semibold tracking-wide uppercase text-gray-500">Workspace</span>
                <div className="flex h-6 w-6 items-center justify-center rounded-md bg-black text-white text-xs font-bold">
                    V
                </div>
            </div>

            <nav className="flex-1 px-4 py-8 space-y-2">
                <Link href="/dashboard" className="flex items-center px-3 py-2.5 text-sm font-medium rounded-xl hover:bg-[#E5E5EA] transition-colors group">
                    <LayoutDashboard className="h-4 w-4 mr-3 text-gray-500 group-hover:text-black transition-colors" />
                    Queue
                </Link>
                <Link href="/approvals" className="flex items-center px-3 py-2.5 text-sm font-medium rounded-xl hover:bg-[#E5E5EA] transition-colors group">
                    <CheckSquare className="h-4 w-4 mr-3 text-gray-500 group-hover:text-black transition-colors" />
                    Approvals
                </Link>
                <Link href="/sales" className="flex items-center px-3 py-2.5 text-sm font-medium rounded-xl hover:bg-[#E5E5EA] transition-colors group">
                    <ArrowRightLeft className="h-4 w-4 mr-3 text-gray-500 group-hover:text-black transition-colors" />
                    Sales Console
                </Link>
                <Link href="/superadmin" className="flex items-center px-3 py-2.5 text-sm font-medium rounded-xl hover:bg-[#E5E5EA] transition-colors group">
                    <Settings className="h-4 w-4 mr-3 text-gray-500 group-hover:text-black transition-colors" />
                    Admin
                </Link>
                <Link href="/settings" className="flex items-center px-3 py-2.5 text-sm font-medium rounded-xl hover:bg-[#E5E5EA] transition-colors group">
                    <Users className="h-4 w-4 mr-3 text-gray-500 group-hover:text-black transition-colors" />
                    Settings
                </Link>
            </nav>

            <div className="p-4 border-t border-[#E5E5EA]">
                <div className="flex items-center gap-3">
                    <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-gray-200 to-gray-400"></div>
                    <div className="flex flex-col">
                        <span className="text-xs font-semibold">Operator</span>
                        <span className="text-[10px] text-gray-500">ID: OP-001</span>
                    </div>
                </div>
            </div>
        </aside>
    );
}
