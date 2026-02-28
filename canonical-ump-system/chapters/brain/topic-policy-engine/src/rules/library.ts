export type PolicyPredicate = (context: Record<string, any>) => boolean;

export const POLICY_LIBRARY: Record<string, PolicyPredicate> = {
    policy_eviction_threshold_v1: (context) => {
        return typeof context?.months_delinquent === 'number' && context.months_delinquent >= 2;
    },
    policy_spending_limit_v1: (context) => {
        return typeof context?.amount_usd === 'number' && context.amount_usd <= 500;
    }
};
