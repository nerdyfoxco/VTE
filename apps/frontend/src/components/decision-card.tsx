"use client";

import React from "react";
import { DecisionRead } from "@/lib/api";
import { CheckCircle, XCircle, AlertCircle, Clock } from "lucide-react";

interface DecisionCardProps {
    decision: DecisionRead;
    onApprove?: (id: string) => void;
    onDeny?: (id: string) => void;
}

export function DecisionCard({ decision, onApprove, onDeny }: DecisionCardProps) {
    const isProposed = decision.outcome === "PROPOSED";

    return (
        <div className="bg-white px-4 py-5 border-b border-gray-200 sm:px-6 hover:bg-gray-50 transition-colors duration-150">
            <div className="flex space-x-3">
                <div className="flex-shrink-0">
                    {decision.outcome === "APPROVED" && <CheckCircle className="h-6 w-6 text-green-500" />}
                    {decision.outcome === "DENIED" && <XCircle className="h-6 w-6 text-red-500" />}
                    {decision.outcome === "PROPOSED" && <Clock className="h-6 w-6 text-yellow-500" />}
                    {decision.outcome === "NEEDS_MORE_EVIDENCE" && <AlertCircle className="h-6 w-6 text-orange-500" />}
                </div>
                <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-gray-900">
                        {decision.intent_action} <span className="text-gray-500">on</span> {decision.intent_target}
                    </p>
                    <p className="text-sm text-gray-500">
                        Actor: {decision.actor_user_id} ({decision.actor_role})
                    </p>
                    <div className="mt-2 text-xs text-gray-400 font-mono">
                        Hash: {decision.decision_hash.substring(0, 12)}...
                    </div>
                    <div className="mt-2 text-xs text-gray-500">
                        {new Date(decision.timestamp).toLocaleString()}
                    </div>
                </div>
                {isProposed && (
                    <div className="flex-shrink-0 self-center flex space-x-2">
                        <button
                            onClick={() => onApprove?.(decision.decision_id)}
                            className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                            Approve
                        </button>
                        <button
                            onClick={() => onDeny?.(decision.decision_id)}
                            className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        >
                            Deny
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
