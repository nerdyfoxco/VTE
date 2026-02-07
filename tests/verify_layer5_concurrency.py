import asyncio
import sys
import os
import time



# Add cwd to path for vte package resolution
sys.path.append(os.getcwd())
try:
    from vte.core.concurrency import guard, TENANT_LIMIT
except ImportError as e:
    print(f"FAIL: Could not import vte.core.concurrency: {e}")
    sys.exit(1)

async def simulate_request(tenant_id: str, hold_time: float):
    """
    Simulates a request attempting to acquire strict limits.
    Directly tests the guard logic since firing up 1000 real HTTP requests
    in this test harness requires uvicorn running.
    We test the logic core (T-1100).
    """
    tenant_sem = guard.get_tenant_semaphore(tenant_id)
    
    # Check Fail Fast
    if guard.global_semaphore._value <= 0:
        return 503
    if tenant_sem._value <= 0:
        return 429
        
    async with guard.global_semaphore:
        async with tenant_sem:
            await asyncio.sleep(hold_time)
            return 200

async def verify_concurrency_logic():
    print("Verifying Layer 5: Concurrency Envelope (T-1100)...")
    
    # 1. Fill the tenant bucket
    print(f"Holding {TENANT_LIMIT} connections...")
    tasks = []
    # Launch exactly the limit
    for _ in range(TENANT_LIMIT):
        tasks.append(asyncio.create_task(simulate_request("tenant_A", 0.5)))
    
    # Give them a moment to acquire
    await asyncio.sleep(0.1)
    
    # 2. Try one more - should fail fast
    print("Attempting overflow request...")
    status = await simulate_request("tenant_A", 0.1)
    
    if status == 429:
        print("PASS: Request rejected with 429 (Tenant Limit).")
    else:
        print(f"FAIL: Request returned {status} but expected 429.")
        sys.exit(1)
        
    # Wait for drain
    await asyncio.gather(*tasks)
    print("Drain complete.")
    
    # 3. Operations should return to normal
    status = await simulate_request("tenant_A", 0.0)
    if status == 200:
        print("PASS: System recovered after load drain.")
    else:
        print(f"FAIL: System stuck in rejection state {status}.")
        sys.exit(1)

    print("LAYER 5 VERIFIED.")

if __name__ == "__main__":
    asyncio.run(verify_concurrency_logic())
