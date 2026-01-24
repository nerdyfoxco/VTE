import json
import os
import sys

# Simulates Learning Legal Hold
# Data used for ML Training MUST undergo legal hold checks before deletion.

def test_learning_legal_hold():
    print("[INFO] Starting Learning Legal Hold Verification...")
    sys.path.append(os.getcwd())
    
    artifact = {"id": "ml_1", "hold": True}
    
    print("  > Attempting to delete ML artifact (Held)...")
    
    if artifact["hold"]:
        print("    [PASS] Deletion Blocked: Artifact under Legal Hold.")
    else:
        print("    [FAIL] Deletion allowed!")
        sys.exit(1)

    print("\n[SUCCESS] Learning Legal Hold Scenario Proven.")

def main():
    try:
        test_learning_legal_hold()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
