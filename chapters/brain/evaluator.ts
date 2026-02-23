import * as fs from 'fs';
import * as path from 'path';

interface DecisionGraph {
    rules: {
        conditions: Record<string, any>;
        action: 'APPROVED' | 'HOLD' | 'STOP';
        reasonCode: string;
    }[];
}

export class DecisionEvaluator {
    private graph: DecisionGraph;

    constructor(graphPath: string) {
        if (!fs.existsSync(graphPath)) {
            throw new Error(`[Evaluator] Missing dependency: ${graphPath} not found. Cannot boot Brain Runtime without deterministic rules.`);
        }
        this.graph = JSON.parse(fs.readFileSync(graphPath, 'utf8'));
    }

    /**
     * Statically evaluate the evidence context against the compiled DAG.
     */
    public evaluate(context: Record<string, any>): { action: string, reason: string } {
        // Enforce a fail-closed default. If rules do not definitively match, route to Supervisor.
        let finalAction = 'HOLD';
        let finalReason = 'AMBIGUOUS_EVIDENCE_NO_RULE_MATCH';

        // Linear rule evaluation. First definitive match wins.
        for (const rule of this.graph.rules) {
            let match = true;
            for (const [key, expectedVal] of Object.entries(rule.conditions)) {
                if (context[key] !== expectedVal) {
                    match = false;
                    break;
                }
            }

            if (match) {
                finalAction = rule.action;
                finalReason = rule.reasonCode;
                // Precedence: STOP overrides HOLD overrides APPROVED, but linear processing
                // halts on the first explicit trigger mapping for the context.
                break;
            }
        }

        return { action: finalAction, reason: finalReason };
    }
}
