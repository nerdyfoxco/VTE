"use client";
import React, { useEffect, useState } from "react";
import { getQueueItems, QueueItem } from "@/lib/api";

/**
 * Headless Surface for Visual Agents (T-0200)
 * 
 * This page is optimized for machine readability by Playwright/Selenium agents.
 * - Minimal styling
 * - Semantic IDs (stable contracts)
 * - Raw data exposure
 */
export default function AgentHeadlessSurface() {
    const [items, setItems] = useState<QueueItem[]>([]);
    const [lastRefreshed, setLastRefreshed] = useState<string>("");

    useEffect(() => {
        refreshData();
    }, []);

    const refreshData = async () => {
        try {
            const data = await getQueueItems();
            setItems(data);
            setLastRefreshed(new Date().toISOString());
        } catch (e) {
            console.error("Agent data fetch failed", e);
        }
    };

    return (
        <div id="vte-agent-surface">
            <h1>VTE Headless Agent Interface</h1>

            <div id="meta-status">
                <span id="agent-status">READY</span>
                <span id="last-refreshed">{lastRefreshed}</span>
                <button id="btn-refresh" onClick={refreshData}>Refresh Data</button>
                {/* Bound Action: Audit Export */}
                <button id="btn_export_audit">Export Audit</button>
            </div>

            <hr />

            <div id="queue-container">
                {items.map((item) => (
                    <div
                        key={item.id}
                        id={`queue-item-${item.id}`}
                        className="agent-queue-item"
                        data-priority={item.priority}
                        data-status={item.status}
                        data-sla={item.sla_deadline}
                    >
                        <div id={`queue-item-${item.id}-title`}>{item.title}</div>
                        <div id={`queue-item-${item.id}-assigned`}>{item.assigned_to}</div>

                        {/* Agent Actions - Deterministic Bindings */}
                        <div className="actions">
                            {item.title.includes("Approve Payment") ? (
                                <button id="btn_approve_invoice">Approve Invoice</button>
                            ) : (
                                <button id={`btn-process-${item.id}`}>Process Item</button>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            <div id="debug-raw-json" style={{ display: 'none' }}>
                {JSON.stringify(items)}
            </div>
        </div>
    );
}
