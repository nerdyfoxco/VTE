export interface IAppFolioReader {
    fetchLedger(unitId: string): { status: 'found' | 'not_found', payload: any };
    fetchDelinquencies(): { status: 'found' | 'not_found', payload: any };
}

export const appfolioReaderAdapter: IAppFolioReader = {
    fetchLedger(unitId: string) {
        console.log(`[READER] Fetching AppFolio Ledger for ${unitId}...`);
        return {
            status: 'found',
            payload: {
                unit_id: unitId,
                current_balance: 0.00,
                recent_transactions: [
                    { type: 'payment', amount: -1500, date: new Date().toISOString() }
                ]
            }
        };
    },

    fetchDelinquencies() {
        console.log(`[READER] Fetching AppFolio Delinquency Global Report...`);
        return {
            status: 'found',
            payload: {
                delinquent_units: ['unit_105', 'unit_200'],
                total_outstanding: 3500.00
            }
        };
    }
};
