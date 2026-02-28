'use client';

import * as React from 'react';
import { Bell, Search, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';

export function VteTopNav() {
    return (
        <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-border bg-background/80 px-6 backdrop-blur-md transition-all">
            <div className="flex items-center gap-4 pl-16 md:pl-0">
                <h1 className="text-sm font-semibold tracking-tight text-foreground/90">
                    VTE Operations <span className="opacity-40 font-normal">/ Production</span>
                </h1>
            </div>

            <div className="flex items-center gap-4">
                {/* Placeholder Global Action: Search */}
                <Button variant="ghost" size="icon" className="text-muted-foreground">
                    <Search className="h-4 w-4" />
                    <span className="sr-only">Search</span>
                </Button>

                {/* Alerts / Context */}
                <Button variant="ghost" size="icon" className="text-muted-foreground relative">
                    <Bell className="h-4 w-4" />
                    <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-destructive" />
                    <span className="sr-only">Notifications</span>
                </Button>

                {/* Auth / Avatar Context */}
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="relative h-8 w-8 rounded-full overflow-hidden">
                            <Avatar className="h-8 w-8 transition-transform hover:scale-105 shadow-sm">
                                <AvatarImage src="" alt="Avatar" className="h-full w-full object-cover" />
                                <AvatarFallback className="bg-primary/10 text-primary text-xs font-semibold h-full w-full flex items-center justify-center">
                                    <User className="h-4 w-4" />
                                </AvatarFallback>
                            </Avatar>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent className="w-56" align="end" forceMount>
                        <DropdownMenuLabel className="font-normal">
                            <div className="flex flex-col space-y-1">
                                <p className="text-sm font-medium leading-none">System Operator</p>
                                <p className="text-xs leading-none text-muted-foreground">operator@vte.example</p>
                            </div>
                        </DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>Profile Settings</DropdownMenuItem>
                        <DropdownMenuItem>Team Management</DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="text-destructive focus:text-destructive">
                            Log out
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </header>
    );
}
