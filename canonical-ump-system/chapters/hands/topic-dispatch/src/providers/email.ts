// Canonical UMP Framework - Hands (External Provider)
// Strict boundaries enclosing third-party logic (e.g., SendGrid, Mailgun)

export interface EmailPayload {
    to: string;
    subject: string;
    body: string;
}

export interface EmailProviderContext {
    providerName: string;
    sendEmail(payload: EmailPayload): Promise<boolean>;
}

export class MockEmailProvider implements EmailProviderContext {
    providerName = "MockSendGrid";

    async sendEmail(payload: EmailPayload): Promise<boolean> {
        console.log(`[HANDS_DISPATCH] simulated external call: ${this.providerName} -> ${payload.to}`);
        console.log(`[HANDS_DISPATCH] Subject: ${payload.subject}`);
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 50));
        return true;
    }
}

import * as nodemailer from 'nodemailer';

export class LiveEmailProvider implements EmailProviderContext {
    providerName = "Canonical Nodemailer SMTP";
    private transporter: nodemailer.Transporter | null = null;

    constructor() {
        this.initializeTransporter();
    }

    private async initializeTransporter() {
        // Automatically generate a real external SMTP test account on Ethereal Email
        // This validates external network egress and standard protocol formatting
        // without accidentally spamming live addresses during tests.
        const testAccount = await nodemailer.createTestAccount();

        this.transporter = nodemailer.createTransport({
            host: testAccount.smtp.host,
            port: testAccount.smtp.port,
            secure: testAccount.smtp.secure,
            auth: {
                user: testAccount.user,
                pass: testAccount.pass,
            }
        });
        console.log(`[HANDS_DISPATCH] Live SMTP Connection Established: ${testAccount.user}`);
    }

    async sendEmail(payload: EmailPayload): Promise<boolean> {
        if (!this.transporter) {
            console.error(`[HANDS_DISPATCH] Transporter not ready yet. Please retry.`);
            return false;
        }

        try {
            console.log(`[HANDS_DISPATCH] Preparing external transmission: ${this.providerName} -> ${payload.to}`);

            // Generate the physical SMTP package
            const info = await this.transporter.sendMail({
                from: '"VTE Canonical System" <canonical@nerdyfox.co>',
                to: payload.to,
                subject: payload.subject,
                text: payload.body,
                html: `<b>${payload.body}</b>`
            });

            console.log(`[HANDS_DISPATCH] SMTP Packet successfully accepted by relay: ${info.messageId}`);

            // Provide a direct internet URL to preview the actual successfully rendered payload
            const previewUrl = nodemailer.getTestMessageUrl(info);
            console.log(`[HANDS_DISPATCH] 🌐 View physical execution trace: ${previewUrl}`);

            return true;
        } catch (error) {
            console.error(`[HANDS_DISPATCH_NATIVE_FAULT] Canonical SMTP Engine crashed transmission:`, error);
            return false;
        }
    }
}
