import { Ajv } from 'ajv';
import * as schema from './pipe-envelope.schema.json';

const ajv = new Ajv();
const validate = ajv.compile(schema);

export function enforcePipeEnvelope(event: any): any {
    if (!validate(event)) {
        throw new Error(`[SpineGuard] Invalid PipeEnvelope: ${ajv.errorsText(validate.errors)}`);
    }

    // Hard invariants per VTE 3.0 Doc
    if (!event.workspace_id) throw new Error('[SpineGuard] Missing workspace_id');
    if (!event.correlation_id) throw new Error('[SpineGuard] Missing correlation_id');
    if (!event.work_item_id) throw new Error('[SpineGuard] Missing work_item_id');

    return event;
}
