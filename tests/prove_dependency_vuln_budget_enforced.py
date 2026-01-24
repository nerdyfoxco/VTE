import json
import os
import sys

# Simulates Dependency Vulnerability Budget
# We allow 0 Critical, max 2 High vulnerabilities.

def test_dep_vuln_budget():
    print("[INFO] Starting Dependency Vuln Budget Verification...")
    sys.path.append(os.getcwd())
    
    # Mock Scan Result
    scan_report = {
        "CRITICAL": 1,
        "HIGH": 1,
        "MEDIUM": 5
    }
    
    print(f"  > Scan Report: {scan_report}")
    
    budget = {
        "CRITICAL": 0,
        "HIGH": 2
    }
    
    # Policy Check
    failed = False
    if scan_report["CRITICAL"] > budget["CRITICAL"]:
        print("    [PASS] Budget Breached: Critical > 0")
        failed = True
        
    if not failed:
        print("    [FAIL] Budget breach should have been detected.")
        sys.exit(1)
        
    print("\n[SUCCESS] Dependency Vuln Budget Scenario Proven.")

def main():
    try:
        test_dep_vuln_budget()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
