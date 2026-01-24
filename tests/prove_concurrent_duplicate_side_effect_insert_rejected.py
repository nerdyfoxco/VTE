import concurrent.futures
import sqlite3
import time
import sys
import uuid

# Proof: Concurrent Duplicate Side-Effect Rejected
# Simulates race condition where two workers try to execute the same external action.

DB_PATH = ":memory:" # Fast emulation

def setup_db(conn):
    conn.execute("""
    CREATE TABLE side_effect_ledger (
        id TEXT PRIMARY KEY,
        idempotency_key TEXT UNIQUE NOT NULL,
        status TEXT
    );
    """)

def attempt_insert(worker_id, key):
    con = sqlite3.connect(DB_PATH) # In-memory sharing logic varies, but for threading demo in same process:
    # Actually sqlite :memory: is per-connection unless shared cache used. 
    # For robust canary, we just mock the IntegrityError behavior if using a real DB stub logic.
    # But let's try to use a shared connection object or file for truth.
    
    # Using file db for concurrency test
    con = sqlite3.connect("vte_canary_race.db") 
    
    try:
        con.execute("INSERT INTO side_effect_ledger (id, idempotency_key, status) VALUES (?, ?, ?)",
                   (str(uuid.uuid4()), key, "PENDING"))
        con.commit()
        return (worker_id, True)
    except sqlite3.IntegrityError:
        return (worker_id, False) # Dup rejected
    finally:
        con.close()

def prove_race_condition_safety():
    print("Testing Side-Effect Ledger Concurrency...")
    
    # Init DB
    con = sqlite3.connect("vte_canary_race.db")
    con.execute("DROP TABLE IF EXISTS side_effect_ledger")
    setup_db(con)
    con.close()
    
    target_key = "idemp_payment_123"
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(attempt_insert, i, target_key) for i in range(5)]
        results = [f.result() for f in futures]
    
    success_count = sum(1 for _, success in results if success)
    fail_count = sum(1 for _, success in results if not success)
    
    print(f"  Attempts: 5")
    print(f"  Successes: {success_count}")
    print(f"  Rejections: {fail_count}")
    
    if success_count == 1 and fail_count == 4:
        print("  [PASS] Exactly ONE insert succeeded. Race condition defeated.")
        return True
    else:
         print("  [FAIL] Invariant violated!")
         return False

if __name__ == "__main__":
    import os
    if prove_race_condition_safety():
        try:
            os.remove("vte_canary_race.db")
        except:
            pass
        sys.exit(0)
    else:
        sys.exit(1)
