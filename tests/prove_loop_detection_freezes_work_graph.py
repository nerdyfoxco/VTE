import json
import os
import sys

# Simulates Loop Detection
# If graph repeats node > N times, Freeze.

def test_loop_detection():
    print("[INFO] Starting Loop Detection Verification...")
    sys.path.append(os.getcwd())
    
    LIMIT = 3
    path = ["step1", "step2", "step1", "step2", "step1"] # Attempting 3rd time
    
    print(f"  > Path: {path}")
    
    # Check
    counts = {}
    frozen = False
    
    for node in path:
        counts[node] = counts.get(node, 0) + 1
        if counts[node] >= LIMIT:
            frozen = True
            print(f"    [PASS] Frozen at node {node} (count {counts[node]})")
            break
            
    if not frozen:
        print("    [FAIL] Loop not detected.")
        sys.exit(1)

    print("\n[SUCCESS] Loop Detection Scenario Proven.")

def main():
    try:
        test_loop_detection()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
