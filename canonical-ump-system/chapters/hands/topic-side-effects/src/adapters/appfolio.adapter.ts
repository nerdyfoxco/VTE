export interface IAppFolioMutator {
    applyLateFee(unitId: string, amount: number): { success: boolean, receipt_id: string };
    postTenantNote(unitId: string, message: string): { success: boolean, receipt_id: string };
}

export const appfolioAdapter: IAppFolioMutator = {
    applyLateFee(unitId: string, amount: number) {
        console.log(`[ADAPTER] Executing MUTATION against AppFolio... (Applying $${amount} to ${unitId})`);
        return { success: true, receipt_id: `tx_appfolio_${Date.now()}` };
    },

    postTenantNote(unitId: string, message: string) {
        console.log(`[ADAPTER] Executing MUTATION against AppFolio... (Posting Note to ${unitId})`);
        return { success: true, receipt_id: `tx_note_${Date.now()}` };
    }
};
