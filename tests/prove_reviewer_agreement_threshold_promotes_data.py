import json
import os
import sys

# Contract paths
PROMOTION_PIPELINE = "contracts/learning/promotion_pipeline_v1.json"
LEARNING_LOOP = "contracts/learning/learning_loop_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class DataPromoter:
    def __init__(self, pipeline_config):
        self.config = pipeline_config
        
    def evaluate_item(self, item_id, reviews):
        min_revs = self.config['thresholds']['min_reviewers']
        if len(reviews) < min_revs:
            return "PENDING_MORE_REVIEWS"
            
        # Calculate agreement (simplified: verify unanimous or high % match)
        # Using simple majority for this test
        labels = [r['label'] for r in reviews]
        most_common = max(set(labels), key=labels.count)
        count = labels.count(most_common)
        agreement = count / len(reviews)
        
        target = self.config['thresholds']['agreement_score']
        
        if agreement >= target:
             return self.config['actions']['promote']
        else:
             return self.config['actions']['demote']

def test_reviewer_agreement():
    print("[INFO] Loading Contracts...")
    pipeline = load_json(PROMOTION_PIPELINE)
    promoter = DataPromoter(pipeline)
    
    # 1. Test Pending
    print("  > Testing insufficient reviews...")
    res = promoter.evaluate_item("item_1", [{"label": "A"}, {"label": "A"}])
    if res != "PENDING_MORE_REVIEWS":
         print(f"[FAIL] Expected PENDING, got {res}")
         sys.exit(1)
    print("[PASS] Insufficient reviews -> PENDING.")
    
    # 2. Test Promotion (High Agreement)
    print("  > Testing high agreement...")
    reviews = [{"label": "A"}, {"label": "A"}, {"label": "A"}]
    res = promoter.evaluate_item("item_2", reviews)
    if res != "ADD_TO_GOLDEN_SET":
         print(f"[FAIL] Expected ADD_TO_GOLDEN_SET, got {res}")
         sys.exit(1)
    print("[PASS] High agreement -> PROMOTED.")
    
    # 3. Test Demotion (Low Agreement)
    print("  > Testing low agreement...")
    reviews_mixed = [{"label": "A"}, {"label": "B"}, {"label": "C"}]
    res = promoter.evaluate_item("item_3", reviews_mixed)
    if res != "FLAG_FOR_AUDIT":
         print(f"[FAIL] Expected FLAG_FOR_AUDIT, got {res}")
         sys.exit(1)
    print("[PASS] Low agreement -> FLAGGED.")

def main():
    try:
        test_reviewer_agreement()
        print("\n[SUCCESS] Reviewer Agreement Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
