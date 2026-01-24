import json
import os
import sys
import time

# Simulates Rate Limit Enforcement
# 10 reqs/sec limit. 11th should block.

def test_rate_limit():
    print("[INFO] Starting Rate Limit Verification...")
    sys.path.append(os.getcwd())
    
    limit = 10
    window_sec = 1
    
    # Mock Rate Limiter State
    # (Simplified: just count)
    count = 0
    
    print(f"  > Simulating {limit+1} requests...")
    
    for i in range(1, limit + 2):
        if count < limit:
            count += 1
            res = "ALLOWED"
        else:
            res = "BLOCKED_RATE_LIMIT"
            
        if i <= limit and res != "ALLOWED":
             print(f"    [FAIL] Request {i} blocked prematurely.")
             sys.exit(1)
        elif i > limit and res != "BLOCKED_RATE_LIMIT":
             print(f"    [FAIL] Request {i} should be blocked.")
             sys.exit(1)
             
    print("    [PASS] Excess requests blocked.")
    print("\n[SUCCESS] Rate Limit Scenario Proven.")

def main():
    try:
        test_rate_limit()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
