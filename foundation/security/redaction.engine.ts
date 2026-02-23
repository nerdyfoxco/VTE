import * as fs from 'fs';
import * as path from 'path';

interface RedactionRule {
    name: string;
    pattern: string;
    replacement: string;
}

interface RedactionConfig {
    rules: RedactionRule[];
    forbidden_fields: string[];
}

const configPath = path.join(__dirname, 'redaction.rules.json');
const config: RedactionConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));

export function redactPayload(payload: any): any {
    if (typeof payload === 'string') {
        let redacted = payload;
        for (const rule of config.rules) {
            const regex = new RegExp(rule.pattern, 'g');
            redacted = redacted.replace(regex, rule.replacement);
        }
        return redacted;
    }

    if (Array.isArray(payload)) {
        return payload.map(item => redactPayload(item));
    }

    if (typeof payload === 'object' && payload !== null) {
        const redactedObj: any = {};
        for (const [key, value] of Object.entries(payload)) {
            if (config.forbidden_fields.includes(key)) {
                redactedObj[key] = '[REDACTED_FIELD]';
            } else {
                redactedObj[key] = redactPayload(value);
            }
        }
        return redactedObj;
    }

    return payload;
}
