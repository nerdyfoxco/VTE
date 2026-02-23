// Hands Module: SendGrid Execution Adapter

export interface EmailPayload {
    to: string;
    subject: string;
    htmlBody: string;
    correlationId: string;
}

export class SendGridAdapter {
    private clientMockActive: boolean = true; // In Prod: sgMail.setApiKey(process.env.SENDGRID_API_KEY)

    public async sendEmail(payload: EmailPayload): Promise<{ success: boolean; messageId?: string; error?: string }> {
        console.log(`[Hands][SendGrid] Preparing Email execution for Correlation ID: ${payload.correlationId}`);

        try {
            if (!this.clientMockActive) {
                throw new Error("SendGrid API credentials missing.");
            }

            // Simulating API latency
            await new Promise(resolve => setTimeout(resolve, 600));

            const mockMsgId = `SG.${Math.random().toString(36).substring(2, 18)}`;
            console.log(`[Hands][SendGrid] -> SUCCESS: Email Dispatched to ${payload.to}. MSG_ID: ${mockMsgId}`);

            return { success: true, messageId: mockMsgId };
        } catch (error: any) {
            console.error(`[Hands][SendGrid] -> FATAL FAILURE: ${error.message}`);
            return { success: false, error: error.message };
        }
    }
}
