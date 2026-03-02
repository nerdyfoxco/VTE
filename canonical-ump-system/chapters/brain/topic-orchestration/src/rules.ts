import { PrismaClient, ExecutionTrace } from '../../../../foundation/node_modules/@prisma/client';

const prisma = new PrismaClient();

export interface RuleEvaluationContext {
    tenantId: string;
    workflowId: string;
    eventPayload: any;
    currentOrgan: string;
}

export class DecisionEngine {
    /**
     * Dynamically fetch all active rules for the tenant based on policy version.
     */
    static async getActiveRules(tenantId: string) {
        return await prisma.decisionRule.findMany({
            where: {
                policy: {
                    tenantId: tenantId,
                    isActive: true
                }
            },
            orderBy: {
                priority: 'asc' // Lower evaluate first
            }
        });
    }

    /**
     * Evaluates a given context against the deterministic Rules Engine stored in Postgres
     */
    static async evaluateContext(context: RuleEvaluationContext): Promise<{ action: string, actionPayload?: string } | null> {
        const rules = await this.getActiveRules(context.tenantId);

        for (const rule of rules) {
            let matched = false;

            // Simplified Evaluation Strategy (Can be extended with JSONPath or full AST parsers)
            switch (rule.conditionType) {
                case "EVENT_SENDER_MATCH":
                    matched = context.eventPayload?.sender === rule.conditionValue;
                    break;
                case "EMAIL_CONTAINS":
                    matched = String(context.eventPayload?.body || "").includes(rule.conditionValue);
                    break;
                case "WORKFLOW_TAG":
                    matched = context.eventPayload?.tags?.includes(rule.conditionValue);
                    break;
                // Default fallback if unknown condition
                default:
                    matched = false;
            }

            if (matched) {
                // Determine Fail-Closed Determinism Action Match
                console.log(`[DECISION_ENGINE] Match Found for Workflow ${context.workflowId}: Rule [${rule.id}] -> Triggering ${rule.action}`);
                return {
                    action: rule.action,
                    actionPayload: rule.actionPayload || undefined
                };
            }
        }

        // If no rules exactly matched, fail closed or require human intervention
        console.warn(`[DECISION_ENGINE] No policy matched for Workflow ${context.workflowId}. Defaulting to HITL.`);
        return { action: 'ESCALATE_HITL', actionPayload: '{"reason": "No automation matches found. Fail-closed."}' };
    }
}
