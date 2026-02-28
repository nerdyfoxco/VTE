export const REDACTED_PLACEHOLDER = '[REDACTED]';

export const PII_KEYS = new Set([
    'ssn',
    'password',
    'credit_card',
    'itin',
    'auth_token'
]);

export function redactContext(context: Record<string, any>): Record<string, any> {
    const redacted: Record<string, any> = {};

    for (const [key, value] of Object.entries(context)) {
        if (PII_KEYS.has(key.toLowerCase())) {
            redacted[key] = REDACTED_PLACEHOLDER;
        } else if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            redacted[key] = redactContext(value); // Recursive redaction
        } else {
            redacted[key] = value;
        }
    }

    return redacted;
}
