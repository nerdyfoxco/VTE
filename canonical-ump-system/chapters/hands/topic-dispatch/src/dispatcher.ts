// Canonical UMP Framework - Hands (Dispatch Organ)
// Strictly isolated gateway for processing LIVE side-effects.

import { LiveEmailProvider, EmailPayload } from './providers/email';

export interface ComputedEffect {
    target: string;
    action: string;
    payloadDrop: any;
}

export class SideEffectDispatcher {
    private emailProvider: LiveEmailProvider;

    constructor() {
        this.emailProvider = new LiveEmailProvider();
    }

    /**
     * Iterates over deterministically calculated consequences from the Brain
     * and executes them sequentially.
     * 
     * In a production canonical implementation, this uses idempotent retry policies.
     */
    public async dispatchAll(tenantId: string, effects: ComputedEffect[]): Promise<boolean> {
        console.log(`[DISPATCH_INITIATED] Routing ${effects.length} actions for Tenant ${tenantId}`);

        let allSuccessful = true;

        for (const effect of effects) {
            try {
                const success = await this.routeEffect(effect);
                if (!success) {
                    allSuccessful = false;
                }
            } catch (error) {
                console.error(`[DISPATCH_FAULT] Error firing ${effect.target}.${effect.action}:`, error);
                allSuccessful = false;
            }
        }

        return allSuccessful;
    }

    private async routeEffect(effect: ComputedEffect): Promise<boolean> {
        switch (effect.target) {
            case 'SENDGRID_API':
                if (effect.action === 'SEND_TEMPLATE' || effect.action === 'EMAIL_TENANT') {
                    // Map the generic effect into the strict EmailPayload shape
                    const emailPayload: EmailPayload = {
                        to: 'tenant@example.com', // Would normally be pulled from payloadDrop
                        subject: `VTE Workflow Notification`,
                        body: String(effect.payloadDrop)
                    };
                    return await this.emailProvider.sendEmail(emailPayload);
                }
                break;
            case 'APPFOLIO_API':
                console.log(`[HANDS_DISPATCH] Handled simulated AppFolio API call for action: ${effect.action}`);
                return true;
            default:
                console.warn(`[DISPATCH_WARNING] Unrecognized effect target: ${effect.target}`);
                return false;
        }
        return false;
    }
}
