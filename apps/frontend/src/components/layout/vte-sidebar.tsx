'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
    LayoutDashboard,
    ListTodo,
    ShieldCheck,
    LineChart,
    Settings,
    BrainCircuit
} from 'lucide-react';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

const routes = [
    { href: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { href: '/queue', icon: ListTodo, label: 'Work Queue' },
    { href: '/approvals', icon: ShieldCheck, label: 'Approvals Inbox' },
    { href: '/sales', icon: LineChart, label: 'Sales Pipeline' },
    { href: '/superadmin', icon: BrainCircuit, label: 'Super Admin' },
    { href: '/settings', icon: Settings, label: 'Settings' }
];

export function VteSidebar() {
    const pathname = usePathname();

    return (
        <TooltipProvider delayDuration={0}>
            <div className="flex h-screen w-[72px] flex-col items-center border-r border-border bg-card py-6 shadow-sm z-50 fixed left-0 top-0">

                {/* Brand Core */}
                <div className="mb-8 flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-sm">
                    <span className="text-xl font-bold tracking-tighter">V</span>
                </div>

                {/* Navigation Core */}
                <nav className="flex flex-1 flex-col items-center gap-4 w-full">
                    {routes.map((route) => {
                        const isActive = pathname === route.href || pathname?.startsWith(`${route.href}/`);
                        return (
                            <Tooltip key={route.href}>
                                <TooltipTrigger asChild>
                                    <Link
                                        href={route.href}
                                        className={cn(
                                            "flex h-11 w-11 items-center justify-center rounded-xl transition-all duration-200",
                                            isActive
                                                ? "bg-primary text-primary-foreground shadow-sm scale-110"
                                                : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                                        )}
                                    >
                                        <route.icon className="h-5 w-5" />
                                        <span className="sr-only">{route.label}</span>
                                    </Link>
                                </TooltipTrigger>
                                <TooltipContent side="right" sideOffset={14} className="font-medium text-xs rounded-md px-3 py-1.5 shadow-sm">
                                    {route.label}
                                </TooltipContent>
                            </Tooltip>
                        );
                    })}
                </nav>

                {/* Global Footer (e.g. Profile / Avatar placeholder) */}
                <div className="mt-auto flex flex-col items-center gap-4">
                    <div className="h-2 w-2 rounded-full bg-border" />
                </div>

            </div>
        </TooltipProvider>
    );
}
