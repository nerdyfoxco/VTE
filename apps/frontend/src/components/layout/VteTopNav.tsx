import React from 'react';
import { Bell, Search, Menu } from 'lucide-react';

export default function VteTopNav() {
    return (
        <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-[#E5E5EA] bg-white/80 backdrop-blur-md px-6 shadow-sm">
            <div className="flex items-center gap-4">
                <button className="md:hidden text-gray-500 hover:text-black">
                    <Menu className="h-5 w-5" />
                </button>
                <div className="relative group hidden sm:block">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 group-focus-within:text-black transition-colors" />
                    <input
                        type="text"
                        placeholder="Search tenant ledgers, work items..."
                        className="h-9 w-64 md:w-80 lg:w-96 rounded-full border border-[#E5E5EA] bg-[#F5F5F7] pl-10 pr-4 text-sm outline-none transition-all placeholder:text-gray-400 focus:border-gray-400 focus:bg-white focus:ring-1 focus:ring-gray-200"
                    />
                </div>
            </div>

            <div className="flex items-center gap-4">
                <button className="relative p-2 text-gray-500 hover:text-black transition-colors rounded-full hover:bg-gray-100">
                    <Bell className="h-5 w-5" />
                    <span className="absolute right-1.5 top-1.5 flex h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
                </button>
                <div className="h-8 w-8 overflow-hidden rounded-full border border-gray-200 bg-gray-100">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Operator1" alt="Profile" className="h-full w-full object-cover" />
                </div>
            </div>
        </header>
    );
}
