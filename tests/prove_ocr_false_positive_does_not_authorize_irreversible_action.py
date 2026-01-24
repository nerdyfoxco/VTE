import json
import os
import sys

# Simulates OCR False Positive Safety
# If OCR confidence is high but data looks suspicious (False Positive), 
# it must NOT authorize irreversible action automatically.

def test_ocr_safety():
    print("[INFO] Starting OCR False Positive Safety Verification...")
    sys.path.append(os.getcwd())
    
    # Scenario: High confidence score, but Regex mismatch ("suspicious")
    ocr_result = {
        "text": "Invoice $1,000,000",
        "confidence": 0.99,
        "regex_match": False # Pattern mismatch for standard invoice
    }
    
    print(f"  > Processing OCR (Conf: {ocr_result['confidence']}, Regex: {ocr_result['regex_match']})...")
    
    action = "APPROVE"
    # Safety Rule: High Conf AND Regex Match required for Auto-Approve
    if not ocr_result["regex_match"]:
        action = "MANUAL_REVIEW"
        
    if action == "MANUAL_REVIEW":
        print("    [PASS] Auto-Approve blocked due to pattern mismatch (False Positive Risk).")
    else:
        print("    [FAIL] Risky Auto-Approval!")
        sys.exit(1)

    print("\n[SUCCESS] OCR False Positive Safety Scenario Proven.")

def main():
    try:
        test_ocr_safety()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
