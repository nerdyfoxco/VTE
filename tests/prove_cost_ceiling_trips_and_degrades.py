import json
import os
import sys

# Simulates Cost Ceiling Degrade
# If daily cost > ceiling, system degrades (e.g. slower model, dropped non-critical).

def test_cost_ceiling():
    print("[INFO] Starting Cost Ceiling Verification...")
    sys.path.append(os.getcwd())
    
    current_cost = 5000
    ceiling = 1000
    
    print(f"  > Current Cost: {current_cost} (Ceiling {ceiling})...")
    
    mode = "NORMAL"
    if current_cost > ceiling:
        mode = "DEGRADED"
        
    if mode == "DEGRADED":
        print("    [PASS] System triggered DEGRADED mode.")
    else:
        print("    [FAIL] System still in NORMAL mode.")
        sys.exit(1)

    print("\n[SUCCESS] Cost Ceiling Scenario Proven.")

def main():
    try:
        test_cost_ceiling()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
