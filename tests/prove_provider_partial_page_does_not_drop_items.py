import sys

# Proof: Partial Page Drop Safety
# Ensures that we do not advance the 'High Watermark' (cursor) if any item in a batch fails to ingest.

class MockSyncEngine:
    def __init__(self):
        self.high_watermark = 0
        self.db = []
        
    def process_page(self, page_items):
        # Transactional simulation
        # If ANY item fails, we rollback and do NOT update high_watermark
        
        temp_ingest = []
        try:
            for item in page_items:
                if item == "CORRUPT_ITEM":
                    raise ValueError("Ingest Failed")
                temp_ingest.append(item)
            
            # Commit
            self.db.extend(temp_ingest)
            self.high_watermark += len(page_items)
            return True
        except ValueError:
            # Rollback
            return False

def prove_partial_drop_safety():
    print("Testing Partial Page Drop Safety...")
    engine = MockSyncEngine()
    
    # 1. Process Good Page
    engine.process_page(["msg1", "msg2"])
    print(f"  Batch 1 (Good): Watermark = {engine.high_watermark}")
    if engine.high_watermark != 2:
        print("  [FAIL] Watermark failed to advance on success.")
        return False
        
    # 2. Process Bad Page (Partial Drop)
    print("  Batch 2 (Contains Limit): ...")
    success = engine.process_page(["msg3", "CORRUPT_ITEM", "msg4"])
    
    if success:
        print("  [FAIL] Engine reported success on corrupt batch!")
        return False
        
    print(f"  Batch 2 Result: Watermark = {engine.high_watermark}")
    
    if engine.high_watermark == 2:
        print("  [PASS] Watermark stayed at 2. No data loss (will retry).")
        return True
    else:
        print(f"  [FAIL] Watermark advanced to {engine.high_watermark} despite failure! Data Gap Created.")
        return False

if __name__ == "__main__":
    if prove_partial_drop_safety():
        sys.exit(0)
    else:
        sys.exit(1)
