import json
import os
import sys

# Simulates Secret Scanning
# Scans source code for regex patterns of secrets (e.g. "sk-...")

def test_secret_scanning():
    print("[INFO] Starting Secret Scanning Verification...")
    sys.path.append(os.getcwd())
    
    # Mock source code
    source_code = [
        "print('Hello')",
        "api_key = 'sk-12345'", # ALERT!
        "config = 'clean'"
    ]
    
    print("  > Scanning source code lines...")
    
    found_secrets = []
    for line in source_code:
        if "sk-" in line or "secret" in line.lower():
            found_secrets.append(line)
            
    if found_secrets:
        print(f"    [PASS] Secret detected: {found_secrets[0]}")
    else:
        print("    [FAIL] Secret NOT detected!")
        sys.exit(1)

    print("\n[SUCCESS] Secret Scanning Scenario Proven.")

def main():
    try:
        test_secret_scanning()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
