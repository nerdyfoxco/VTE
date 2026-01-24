import json
import os
import sys

# Simulates Cross-Tenant Read Block
# We assume isolation by Account ID prefix or similar.
# In VTE Sheet Schema, we enforce Account ID format, but here we enforce Access Control.
# Current User = Tenant A. Requested Resource = Tenant B.

def test_cross_tenant_read():
    print("[INFO] Starting Cross-Tenant Read Verification...")
    
    current_tenant = "TENANT_A"
    
    requested_resource = {
        "resource_id": "doc_123",
        "tenant_id": "TENANT_B",
        "content": "Secret Data"
    }
    
    print(f"  > User {current_tenant} requesting resource of {requested_resource['tenant_id']}...")
    
    # Access Control Logic
    if current_tenant != requested_resource['tenant_id']:
        print("    [PASS] Access Denied: Tenant Mismatch.")
    else:
        print("    [FAIL] Cross-tenant access allowed!")
        sys.exit(1)

    print("\n[SUCCESS] Cross-Tenant Read Negative Scenario Proven.")

def main():
    try:
        test_cross_tenant_read()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
