"use client";

import React, { useEffect, useState } from "react";
import { getDecisions, createDecision, DecisionRead } from "@/lib/api";
import { DecisionCard } from "@/components/decision-card";

export default function Dashboard() {
    const [decisions, setDecisions] = useState<DecisionRead[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchCurentDecisions = async () => {
        try {
            setLoading(true);
            const data = await getDecisions();
            setDecisions(data);
        } catch (e) {
            console.error("Failed to fetch decisions", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCurentDecisions();
    }, []);

    const processDecision = async (original: DecisionRead, outcome: "APPROVED" | "DENIED") => {
        if (!confirm(`Are you sure you want to ${outcome} this decision?`)) return;

        try {
            await createDecision({
                actor: {
                    user_id: "admin_vte", // MVP: Mocked Admin
                    role: "super_admin",
                    session_id: "dashboard_session"
                },
                intent: {
                    action: original.intent_action,
                    target_resource: original.intent_target,
                    parameters: original.intent_params
                },
                evidence_hash: original.evidence_hash || "",
                outcome: outcome,
                policy_version: original.policy_version
            });
            // Refresh list to show new block and update pending state
            await fetchCurentDecisions();
        } catch (e) {
            console.error("Failed to process decision", e);
            alert("Error processing decision. Check console.");
        }
    };

    const handleApprove = (id: string) => {
        const decision = decisions.find(d => d.decision_id === id);
        if (decision) processDecision(decision, "APPROVED");
    };

    const handleDeny = (id: string) => {
        const decision = decisions.find(d => d.decision_id === id);
        if (decision) processDecision(decision, "DENIED");
    };

    if (loading) {
        return <div className="p-8 text-center text-gray-500">Loading Governance Data...</div>;
    }

    // Correlation Logic: A Proposal is "Pending" if no other decision exists with the same evidence_hash that is FINAL (Approved/Denied).
    // Note: This assumes 1:1 mapping between Evidence Bundle and Decision flow.
    const finalizedEvidenceHashes = new Set(
        decisions
            .filter(d => d.outcome === "APPROVED" || d.outcome === "DENIED")
            .map(d => d.evidence_hash)
            .filter(Boolean)
    );

    const pending = decisions.filter(d =>
        d.outcome === "PROPOSED" &&
        (!d.evidence_hash || !finalizedEvidenceHashes.has(d.evidence_hash))
    );

    // History excludes Proposals
    const history = decisions.filter(d => d.outcome !== "PROPOSED");

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
                <div className="md:grid md:grid-cols-3 md:gap-6">
                    <div className="md:col-span-1">
                        <h3 className="text-lg font-medium leading-6 text-gray-900">Pending Approvals</h3>
                        <p className="mt-1 text-sm text-gray-500">
                            Decisions proposed by Autonomous Agents requiring human verification.
                        </p>
                    </div>
                    <div className="mt-5 md:mt-0 md:col-span-2">
                        <div className="flex flex-col mb-4">
                            <div className="text-4xl font-bold text-blue-600">{pending.length}</div>
                            <div className="text-sm text-gray-500">Pending Actions</div>
                        </div>

                        <div className="bg-gray-50 rounded-md border border-gray-200 divide-y divide-gray-200">
                            {pending.length === 0 ? (
                                <div className="p-4 text-sm text-gray-500 text-center">No pending approvals. All good!</div>
                            ) : (
                                pending.map(d => (
                                    <DecisionCard
                                        key={d.decision_id}
                                        decision={d}
                                        onApprove={handleApprove}
                                        onDeny={handleDeny}
                                    />
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* History */}
            <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
                <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">Decision History</h3>
                <div className="bg-white rounded-md border border-gray-200 divide-y divide-gray-200">
                    {history.map(d => (
                        <DecisionCard key={d.decision_id} decision={d} />
                    ))}
                </div>
            </div>
        </div>
    );
}
