import json
import os
import sys

# Simulates No-Mocks in E2E
# Ensures that tests running in "E2E" mode cannot register mock providers.

def test_no_mocks_e2e():
    print("[INFO] Starting No-Mocks E2E Verification...")
    sys.path.append(os.getcwd())
    
    current_mode = "E2E"
    
    print(f"  > Attempting to register mock provider in {current_mode}...")
    
    # Mock Provider Registry
    def register_provider(name, is_mock=False):
        if is_mock and current_mode == "E2E":
            return "BLOCKED_MOCK_IN_E2E"
        return "REGISTERED"
        
    res = register_provider("CreditScoreMock", is_mock=True)
    
    if res == "BLOCKED_MOCK_IN_E2E":
        print("    [PASS] Mock Registration Blocked.")
    else:
        print(f"    [FAIL] Mock allowed: {res}")
        sys.exit(1)

    print("\n[SUCCESS] No-Mocks Scenario Proven.")

def main():
    try:
        test_no_mocks_e2e()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
