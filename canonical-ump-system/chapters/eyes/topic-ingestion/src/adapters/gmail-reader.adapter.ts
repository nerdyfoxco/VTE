export interface IGmailReader {
    fetchUnreadEmails(query: string): { status: 'found' | 'not_found', payload: any };
}

export const gmailReaderAdapter: IGmailReader = {
    fetchUnreadEmails(query: string) {
        console.log(`[READER] Fetching Unread Gmails matching query: "${query}"...`);
        return {
            status: 'found',
            payload: {
                emails: [
                    {
                        subject: 'Late Payment Notice',
                        body: 'I will pay tomorrow.',
                        from: 'tenant_105@example.com',
                        date: new Date().toISOString()
                    }
                ]
            }
        };
    }
};
