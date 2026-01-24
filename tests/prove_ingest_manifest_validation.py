import json
import os
import sys

# Contract paths
MANIFEST_SCHEMA = "contracts/ingestion/ingest_manifest_schema.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class ManifestValidator:
    def __init__(self, schema):
        self.schema = schema
        
    def validate(self, manifest):
        # 1. Check File Count
        declared_count = manifest.get('file_count')
        actual_files = manifest.get('files', [])
        
        if len(actual_files) != declared_count:
            return f"FILE_COUNT_MISMATCH: Declared {declared_count}, Found {len(actual_files)}"
            
        # 2. Check Required Fields
        if not manifest.get('manifest_id'): return "MISSING_ID"
        if not manifest.get('source_system'): return "MISSING_SOURCE"
        
        return "VALID"

def test_manifest_validation():
    print("[INFO] Loading Schema...")
    schema = load_json(MANIFEST_SCHEMA)
    validator = ManifestValidator(schema)
    
    # 1. Valid Manifest
    print("  > Testing valid manifest...")
    valid = {
        "manifest_id": "m-1",
        "source_system": "PartnerA",
        "file_count": 2,
        "files": [
            {"filename": "a.csv", "sha256": "123", "row_count": 10},
            {"filename": "b.csv", "sha256": "456", "row_count": 20}
        ],
        "uploaded_by_user": "admin@example.com"
    }
    res = validator.validate(valid)
    if res != "VALID":
        print(f"[FAIL] Expected VALID, got {res}")
        sys.exit(1)
    print("[PASS] Valid manifest accepted.")
    
    # 2. Mismatched Count
    print("  > Testing count mismatch...")
    bad = valid.copy()
    bad['file_count'] = 99
    res = validator.validate(bad)
    if "FILE_COUNT_MISMATCH" not in res:
         print(f"[FAIL] Expected COUNT_MISMATCH, got {res}")
         sys.exit(1)
    print("[PASS] Count mismatch rejected.")

def main():
    try:
        test_manifest_validation()
        print("\n[SUCCESS] Ingest Manifest Validation Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
