import { globalCircuitController } from '../circuit/breaker';

export interface MutatorReceipt {
    status: 'shadow' | 'live';
    target_system: string;
    action: string;
    receipt_id: string;
    parameters: any;
}

export function executeWithSafety(commandPayload: any, adapterFunc: () => any): MutatorReceipt {
    const { action, target_system, parameters, execution_authz } = commandPayload.data;

    // 1. Structural Spam Defense Hook
    globalCircuitController.checkExecutionTolerance(target_system);

    const isMockToken = !execution_authz || execution_authz.token === 'mock' || execution_authz.token === 'dry-run';
    const riskTierIsHigh = execution_authz && execution_authz.risk_tier > 2;

    // Enforce zero-trust default. If the token is fake or risk tier exceeds threshold, block live adapter execution.
    if (isMockToken || riskTierIsHigh) {
        console.log(`[SHADOW ENGINE] Intercepted execution intent. Bypassing adapter: ${target_system}.${action}`);
        return {
            status: 'shadow',
            target_system,
            action,
            receipt_id: `shadow_${Date.now()}`,
            parameters
        };
    }

    console.log(`[LIVE ENGINE] Authorized mutation. Invoking physical adapter: ${target_system}.${action}`);
    const adapterResult = adapterFunc();

    return {
        status: 'live',
        target_system,
        action,
        receipt_id: adapterResult?.receipt_id || `live_${Date.now()}`,
        parameters
    };
}
