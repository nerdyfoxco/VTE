import json
import os
import sys
import fnmatch

# Contract paths
SEALED_PATHS_MANIFEST = "contracts/meta/sealed_paths_manifest_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class ChangeGuardian:
    def __init__(self, manifest):
        self.sealed_patterns = manifest['sealed_paths']
        
    def check_modification(self, file_path, user_role="DEV"):
        file_path = file_path.replace("\\", "/")
        
        is_sealed = False
        for pattern in self.sealed_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                is_sealed = True
                break
                
        if is_sealed:
            if user_role != "SECURITY_ADMIN":
                return "BLOCKED"
        
        return "ALLOWED"

def test_sealed_paths():
    print("[INFO] Loading Sealed Paths Manifest...")
    manifest = load_json(SEALED_PATHS_MANIFEST)
    guardian = ChangeGuardian(manifest)
    
    # 1. Test Regular Dev modifying Sealed Path
    print("[INFO] Testing DEV modifying sealed path...")
    res = guardian.check_modification("contracts/meta/some_critical_policy.json", user_role="DEV")
    if res != "BLOCKED":
        print(f"[FAIL] Sealed path modification allowed for DEV! Result: {res}")
        sys.exit(1)
    print("[PASS] Sealed path modification blocked.")
    
    # 2. Test Security Admin modifying Sealed Path
    print("[INFO] Testing SECURITY_ADMIN modifying sealed path...")
    res = guardian.check_modification("contracts/meta/some_critical_policy.json", user_role="SECURITY_ADMIN")
    if res != "ALLOWED":
         print(f"[FAIL] Sealed path modification blocked for ADMIN! Result: {res}")
         sys.exit(1)
    print("[PASS] Sealed path modification allowed for ADMIN.")

    # 3. Test Unsealed Path
    print("[INFO] Testing DEV modifying unsealed path...")
    res = guardian.check_modification("contracts/features/some_feature.json", user_role="DEV")
    if res != "ALLOWED":
         print(f"[FAIL] Unsealed path modification blocked! Result: {res}")
         sys.exit(1)
    print("[PASS] Unsealed path modification allowed.")

def main():
    try:
        test_sealed_paths()
        print("\n[SUCCESS] Sealed Path Protection Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
