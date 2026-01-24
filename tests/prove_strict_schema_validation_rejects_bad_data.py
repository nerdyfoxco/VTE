import json
import os
import sys
import re

# Contract paths
SHEET_SCHEMA = "contracts/compliance/vte_sheet_schema.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class RowValidator:
    def __init__(self, schema):
        self.schema = schema
        self.columns = schema['columns']
        
    def validate(self, row):
        errors = []
        # Check required
        for col, rules in self.columns.items():
            if rules.get('required') and col not in row:
                errors.append(f"Missing required column: {col}")
                continue
                
            if col in row:
                val = row[col]
                # Type Check String
                if rules['type'] == 'STRING':
                    if not isinstance(val, str):
                        errors.append(f"{col}: Expected string")
                    elif 'pattern' in rules:
                         if not re.match(rules['pattern'], val):
                             errors.append(f"{col}: Invalid format '{val}'")
                    elif 'min_length' in rules:
                         if len(val) < rules['min_length']:
                             errors.append(f"{col}: Too short")
                             
                # Type Check Decimal
                elif rules['type'] == 'DECIMAL':
                     if not isinstance(val, (int, float)):
                         errors.append(f"{col}: Expected number")
                     elif 'min_value' in rules:
                         if val < rules['min_value']:
                             errors.append(f"{col}: Value {val} < {rules['min_value']}")

                # Type Check Enum
                elif rules['type'] == 'ENUM':
                     if val not in rules['values']:
                         errors.append(f"{col}: Invalid value '{val}'")

        return errors

def test_schema_validation():
    print("[INFO] Loading Schema...")
    schema = load_json(SHEET_SCHEMA)
    validator = RowValidator(schema)
    
    # 1. Valid Row
    print("  > Testing valid row...")
    valid_row = {
        "account_id": "ACC-12345678",
        "customer_name": "John Doe",
        "balance_due": 100.50,
        "state_code": "NY"
    }
    errs = validator.validate(valid_row)
    if errs:
        print(f"[FAIL] Valid row rejected with errors: {errs}")
        sys.exit(1)
    print("[PASS] Valid row accepted.")
    
    # 2. Invalid Pattern (Account ID)
    print("  > Testing invalid pattern...")
    bad_row = valid_row.copy()
    bad_row['account_id'] = "BAD-ID"
    errs = validator.validate(bad_row)
    if not any("Invalid format" in e for e in errs):
         print(f"[FAIL] Should have caught pattern error. Got: {errs}")
         sys.exit(1)
    print("[PASS] Invalid pattern rejected.")
    
    # 3. Invalid Enum (State)
    print("  > Testing invalid enum...")
    bad_row = valid_row.copy()
    bad_row['state_code'] = "XX"
    errs = validator.validate(bad_row)
    if not any("Invalid value" in e for e in errs):
         print(f"[FAIL] Should have caught enum error. Got: {errs}")
         sys.exit(1)
    print("[PASS] Invalid enum rejected.")

    # 4. Missing Required
    print("  > Testing missing required...")
    bad_row = {"customer_name": "No Account"}
    errs = validator.validate(bad_row)
    if not any("Missing required column: account_id" in e for e in errs):
         print(f"[FAIL] Should have caught missing field. Got: {errs}")
         sys.exit(1)
    print("[PASS] Missing required column rejected.")

def main():
    try:
        test_schema_validation()
        print("\n[SUCCESS] Strict Schema Validation Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
