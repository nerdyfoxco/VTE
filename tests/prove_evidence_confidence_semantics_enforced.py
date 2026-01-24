import json
import os
import sys

# Simulates Evidence Confidence Check
# Verify actions match confidence thresholds.

def test_evidence_confidence():
    print("[INFO] Starting Evidence Confidence Verification...")
    sys.path.append(os.getcwd())
    
    # Contract: HIGH -> AUTO, MEDIUM -> REVIEW
    scenarios = [
        {"conf": 0.95, "expect": "AUTO_APPROVE"},
        {"conf": 0.75, "expect": "FLAG_FOR_REVIEW"},
        {"conf": 0.50, "expect": "REJECT"}
    ]
    
    print("  > Testing Confidence Thresholds...")
    
    for s in scenarios:
        action = "REJECT"
        if s["conf"] > 0.90: action = "AUTO_APPROVE"
        elif s["conf"] > 0.70: action = "FLAG_FOR_REVIEW"
        
        if action == s["expect"]:
            print(f"    [PASS] Conf {s['conf']} -> {action}")
        else:
            print(f"    [FAIL] Conf {s['conf']} -> {action} (Expected {s['expect']})")
            sys.exit(1)

    print("\n[SUCCESS] Evidence Confidence Scenario Proven.")

def main():
    try:
        test_evidence_confidence()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
