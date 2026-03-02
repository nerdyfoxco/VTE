import { GmailClient } from './google';
import axios from 'axios';
import jwt from 'jsonwebtoken';

export class SensesPoller {
    private gmail: GmailClient;
    private intervalId: NodeJS.Timeout | null = null;
    private gatewayUrl: string;

    constructor() {
        this.gmail = new GmailClient();
        // Pointing cleanly at the new Native Node Edge Gateway 
        this.gatewayUrl = process.env.GATEWAY_URL || 'http://localhost:8000/api/v1/orchestration/live';
    }

    private generateSystemToken(): string {
        const secret = process.env.VTE_JWT_SECRET;
        if (!secret) throw new Error("[SENSES] VTE_JWT_SECRET missing. Cannot authorize Brain Dispatch.");

        return jwt.sign({
            tenantId: "00000000-0000-0000-0000-000000000001",
            operatorId: "00000000-0000-0000-0000-000000000009",
            role: "admin",
            email: "system-ingestion@vintasoftware.com",
            jti: "senses_daemon_continuous_session"
        }, secret, { expiresIn: '1h' });
    }

    /**
     * Executes the Core Extraction loop mapping Gmail Senses into the Brain
     */
    async poll() {
        console.log("\n[SENSES] 👁️  Waking up... Sweeping Gmail API for unprocessed ingress context.");

        try {
            // Polling specifically for unread messages locally to prevent infinite ingestion loops
            const emails = await this.gmail.fetchEmails(5, "is:unread label:inbox");
            if (emails.length === 0) {
                console.log("[SENSES] 😴 No new unread messages detected. Sleeping.");
                return;
            }

            console.log(`[SENSES] 📥 Detected ${emails.length} new traces. Handing context to the Brain Engine.`);

            for (const email of emails) {
                console.log(`   -> 📨 Ingesting: [${email.sender}] ${email.subject}`);

                // Formatting payload generically for Canonical UMP schema validation limits
                const payload = {
                    workflowName: "canonical_senses_pipeline",
                    payload: {
                        sourceId: email.source_id,
                        subject: email.subject,
                        sender: email.sender,
                        date: email.date_raw,
                        snippet: email.snippet,
                        context: "gmail_extraction_poller"
                    }
                };

                // Dispatching directly natively to the Canonical Brain securely
                try {
                    const systemToken = this.generateSystemToken();

                    const response = await axios.post(this.gatewayUrl, payload, {
                        headers: {
                            Authorization: `Bearer ${systemToken}`
                        }
                    });
                    console.log(`   -> 🧠 Brain Dispatch Complete! Response: ${response.data.status} | Trace: ${response.data.traceId}`);

                    // Mark as read or remove label (mocked for now, depending on Production scopes)
                } catch (e: any) {
                    console.error(`   -> ❌ Brain Dispatch failed for Trace ${email.source_id}:`, e.message);
                }
            }

        } catch (e: any) {
            console.error("[SENSES] 🚨 Critical failure in the ingestion logic loop:", e.message);
        }
    }

    start(intervalMs = 60000) {
        console.log(`[SENSES] 🚀 Starting Background Senses Daemon natively (${intervalMs}ms cycle)`);
        this.poll(); // Initial boot scan
        this.intervalId = setInterval(() => this.poll(), intervalMs);
    }

    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
            console.log("[SENSES] 🛑 Background Senses Daemon halted.");
        }
    }
}
