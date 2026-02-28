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
