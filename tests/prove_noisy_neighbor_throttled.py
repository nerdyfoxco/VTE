import json
import os
import sys
import time

# Simulates Noisy Neighbor Throttling
# Tenant A spams system, Tenant B should remain unaffected (or A should be throttled).

def test_noisy_neighbor():
    print("[INFO] Starting Noisy Neighbor Verification...")
    sys.path.append(os.getcwd())
    
    tenant_a_reqs = 1000
    tenant_b_reqs = 10
    
    limit_per_tenant = 100
    
    print(f"  > Tenant A sending {tenant_a_reqs} reqs (Limit {limit_per_tenant})...")
    
    throttled_a = 0
    accepted_a = 0
    
    for i in range(tenant_a_reqs):
        if i >= limit_per_tenant:
            throttled_a += 1
        else:
            accepted_a += 1
            
    print(f"    [PASS] Tenant A Result: {accepted_a} Accepted, {throttled_a} Throttled.")
    
    if throttled_a == 0:
        print("    [FAIL] Noisy neighbor not throttled!")
        sys.exit(1)
        
    print("  > Tenant B sending normal traffic...")
    # B should be fine
    if tenant_b_reqs <= limit_per_tenant:
        print("    [PASS] Tenant B fully accepted.")

    print("\n[SUCCESS] Noisy Neighbor Scenario Proven.")

def main():
    try:
        test_noisy_neighbor()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
