import concurrent.futures
import sqlite3
import uuid
import sys

# Proof: Sync Deduplication
# Simulates race condition where multiple sync workers process the same Provider Message ID.

def setup_db(conn):
    conn.execute("""
    CREATE TABLE message_ingest_log (
        id TEXT PRIMARY KEY,
        provider_message_id TEXT UNIQUE NOT NULL,
        status TEXT
    );
    """)

def attempt_ingest(worker_id, provider_msg_id):
    con = sqlite3.connect("vte_sync_race.db") 
    try:
        # Try to insert. The UNIQUE constraint on provider_message_id is the key.
        con.execute("INSERT INTO message_ingest_log (id, provider_message_id, status) VALUES (?, ?, ?)",
                   (str(uuid.uuid4()), provider_msg_id, "INGESTED"))
        con.commit()
        return (worker_id, True)
    except sqlite3.IntegrityError:
        return (worker_id, False) # Dup rejected
    finally:
        con.close()

def prove_dedupe():
    print("Testing Sync Deduplication (Race Condition)...")
    
    con = sqlite3.connect("vte_sync_race.db")
    con.execute("DROP TABLE IF EXISTS message_ingest_log")
    setup_db(con)
    con.close()
    
    msg_id = "gmail_msg_12345"
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(attempt_ingest, i, msg_id) for i in range(5)]
        results = [f.result() for f in futures]
    
    success_count = sum(1 for _, success in results if success)
    fail_count = sum(1 for _, success in results if not success)
    
    print(f"  Attempts: 5")
    print(f"  Successes: {success_count}")
    print(f"  Rejections (Deduped): {fail_count}")
    
    if success_count == 1 and fail_count == 4:
        print("  [PASS] Exactly ONE ingest succeeded. Deduplication Verified.")
        return True
    else:
         print("  [FAIL] Invariant violated! Duplicates allowed or all failed.")
         return False

if __name__ == "__main__":
    import os
    if prove_dedupe():
        try:
            os.remove("vte_sync_race.db")
        except:
            pass
        sys.exit(0)
    else:
        sys.exit(1)
