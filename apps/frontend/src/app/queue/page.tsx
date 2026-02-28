"use client";

import React, { useState } from 'react';
import { MoreHorizontal, Filter, AlertCircle, PhoneOff, Play } from 'lucide-react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const mockQueueData = [
    { id: 'WI-9021', location: '3118 N Bambrey St, Phila', tenant: 'Tonette N. Whitehead', amount: '$1,030.00', status: 'HOLD', tag: 'JBA', risk: 'High' },
    { id: 'WI-9022', location: '1540 Edgeley St, Apt 2B', tenant: 'Marcus T. Vance', amount: '$450.00', status: 'STOP', tag: 'DNC', risk: 'Critical' },
    { id: 'WI-9023', location: '8910 Frankford Ave', tenant: 'Sarah Jenkins', amount: '$2,100.00', status: 'PENDING', tag: '3DAY', risk: 'Medium' },
];

export default function WorkQueuePage() {
    const [data] = useState(mockQueueData);
    const [isStarting, setIsStarting] = useState<string | null>(null);

    const startWorkflow = async (workItemId: string) => {
        setIsStarting(workItemId);
        try {
            const orchestratorUrl = process.env.NEXT_PUBLIC_ORCHESTRATOR_URL || 'http://localhost:3001';
            const res = await fetch(`${orchestratorUrl}/workflows/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    workflow_name: 'Eviction_Process',
                    initiator: 'operator@vte.example',
                    inputs: { work_item_id: workItemId }
                })
            });

            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                console.error('Failed to start workflow:', errData);
                alert(`Failed: ${errData.error || res.statusText}`);
            } else {
                const json = await res.json();
                console.log('Workflow Started:', json);
                alert(`Success! Started Workflow ID: ${json.workflow_id}`);
            }
        } catch (err: any) {
            console.error(err);
            alert('Network Error connecting to Canonical Orchestrator.');
        } finally {
            setIsStarting(null);
        }
    };

    return (
        <div className="flex flex-col space-y-6 p-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight">Work Queue (SC-0100)</h1>
                    <p className="text-sm text-muted-foreground mt-1">Manage physical tenant arrears, execution holds, and compliance gates.</p>
                </div>
                <button className="inline-flex items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-sm hover:bg-primary/90 transition-colors">
                    <Filter className="mr-2 h-4 w-4" /> Filter SLA
                </button>
            </div>

            <div className="rounded-md border bg-card">
                <Table>
                    <TableHeader className="bg-muted/50">
                        <TableRow>
                            <TableHead className="w-[120px] font-medium uppercase text-xs tracking-wider">Work Item ID</TableHead>
                            <TableHead className="font-medium uppercase text-xs tracking-wider">Identity & Location</TableHead>
                            <TableHead className="font-medium uppercase text-xs tracking-wider">Target Arrears</TableHead>
                            <TableHead className="font-medium uppercase text-xs tracking-wider">Compliance State</TableHead>
                            <TableHead className="text-right font-medium uppercase text-xs tracking-wider">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {data.map((item) => (
                            <TableRow key={item.id} className="hover:bg-muted/30 transition-colors">
                                <TableCell className="font-mono text-xs font-semibold">{item.id}</TableCell>
                                <TableCell>
                                    <div className="flex flex-col gap-0.5">
                                        <span className="font-semibold text-foreground">{item.tenant}</span>
                                        <span className="text-xs text-muted-foreground">{item.location}</span>
                                    </div>
                                </TableCell>
                                <TableCell className="font-medium">{item.amount}</TableCell>
                                <TableCell>
                                    <div className="flex items-center gap-2">
                                        <Badge
                                            variant={item.status === 'STOP' ? 'destructive' : item.status === 'HOLD' ? 'secondary' : 'outline'}
                                            className="font-semibold uppercase tracking-wider text-[10px]"
                                        >
                                            {item.status}
                                        </Badge>

                                        {item.tag === 'DNC' && (
                                            <span title="Do Not Contact">
                                                <PhoneOff className="h-4 w-4 text-destructive" />
                                            </span>
                                        )}
                                        {item.tag === 'JBA' && (
                                            <span title="Judgment By Agreement">
                                                <AlertCircle className="h-4 w-4 text-amber-500" />
                                            </span>
                                        )}
                                    </div>
                                </TableCell>
                                <TableCell className="text-right">
                                    <div className="flex items-center justify-end gap-2">
                                        <button
                                            onClick={() => startWorkflow(item.id)}
                                            disabled={isStarting === item.id}
                                            className="inline-flex items-center justify-center rounded-md bg-secondary px-3 py-1.5 text-xs font-medium text-secondary-foreground hover:bg-secondary/80 focus:outline-none disabled:opacity-50"
                                        >
                                            {isStarting === item.id ? 'Starting...' : <><Play className="mr-1 h-3 w-3" /> Execute</>}
                                        </button>
                                        <button className="text-muted-foreground hover:text-foreground transition-colors p-1.5 rounded-md hover:bg-muted">
                                            <MoreHorizontal className="h-5 w-5" />
                                        </button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
}
