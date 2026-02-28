import Ajv, { ErrorObject } from 'ajv';
import addFormats from 'ajv-formats';
import fs from 'fs';
import path from 'path';

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

export class ContractRunner {
    private schemaPath: string;
    private validator: any;

    constructor(schemaRelativePath: string) {
        // Navigate up to the repository root from the topic test execution path
        this.schemaPath = path.resolve(process.cwd(), '../../../', schemaRelativePath);
        const schemaContent = fs.readFileSync(this.schemaPath, 'utf8');
        const schema = JSON.parse(schemaContent);
        this.validator = ajv.compile(schema);
    }

    public validate(payload: any): { valid: boolean; errors?: ErrorObject[] | null } {
        const valid = this.validator(payload);
        if (!valid) {
            return { valid: false, errors: this.validator.errors };
        }
        return { valid: true };
    }

    public assertValid(payload: any): void {
        const result = this.validate(payload);
        if (!result.valid) {
            throw new Error(`Contract Violation in ${path.basename(this.schemaPath)}: ${JSON.stringify(result.errors, null, 2)}`);
        }
    }

    public assertInvalid(payload: any): void {
        const result = this.validate(payload);
        if (result.valid) {
            throw new Error(`Expected Contract Violation in ${path.basename(this.schemaPath)}, but payload was valid.`);
        }
    }
}
