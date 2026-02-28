"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ContractRunner = void 0;
const ajv_1 = __importDefault(require("ajv"));
const ajv_formats_1 = __importDefault(require("ajv-formats"));
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const ajv = new ajv_1.default({ allErrors: true, strict: false });
(0, ajv_formats_1.default)(ajv);
class ContractRunner {
    schemaPath;
    validator;
    constructor(schemaRelativePath) {
        // Navigate up to the repository root from the topic test execution path
        this.schemaPath = path_1.default.resolve(process.cwd(), '../../../', schemaRelativePath);
        const schemaContent = fs_1.default.readFileSync(this.schemaPath, 'utf8');
        const schema = JSON.parse(schemaContent);
        this.validator = ajv.compile(schema);
    }
    validate(payload) {
        const valid = this.validator(payload);
        if (!valid) {
            return { valid: false, errors: this.validator.errors };
        }
        return { valid: true };
    }
    assertValid(payload) {
        const result = this.validate(payload);
        if (!result.valid) {
            throw new Error(`Contract Violation in ${path_1.default.basename(this.schemaPath)}: ${JSON.stringify(result.errors, null, 2)}`);
        }
    }
    assertInvalid(payload) {
        const result = this.validate(payload);
        if (result.valid) {
            throw new Error(`Expected Contract Violation in ${path_1.default.basename(this.schemaPath)}, but payload was valid.`);
        }
    }
}
exports.ContractRunner = ContractRunner;
