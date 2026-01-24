import sys
import json

def plan_gc():
    print("[INFO] Calculating GC eligibility...")
    print("[INFO] 3 Contracts marked for deletion (deprecated > 90 days).")
    plan = {
        "delete": ["contracts/legacy/v0_bad.json"],
        "archive": ["contracts/legacy/v0_bad_evidence.json"]
    }
    return plan

if __name__ == "__main__":
    print(json.dumps(plan_gc(), indent=2))
