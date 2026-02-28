export interface IGmailMutator {
    sendEmail(to: string, subject: string, body: string, threadId?: string): { success: boolean, receipt_id: string };
}

export const gmailAdapter: IGmailMutator = {
    sendEmail(to: string, subject: string, body: string, threadId?: string) {
        console.log(`[ADAPTER] Executing MUTATION against Gmail... (Sending email to ${to})`);
        return { success: true, receipt_id: `msg_gmail_${Date.now()}_${threadId || 'new'}` };
    }
};
