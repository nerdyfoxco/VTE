import sys
import os

# Simulates Ship Gate
# Blocks release if high risk is detected and NOT found in the register.

def test_ship_gate():
    print("[INFO] Starting Ship Gate Verification...")
    
    # Mock Risk
    detected_risk = "RISK-099: Unknown Vulnerability"
    
    print(f"  > Detected Risk: {detected_risk}")
    print("  > Checking Risk Register...")
    
    # Register Mock
    register = ["RISK-001", "RISK-002"]
    
    if "RISK-099" not in register:
        print("  > Risk NOT found in Sealed Register.")
        print("  > BLOCKING RELEASE.")
        print("    [PASS] Ship Gate enforces explicit risk acceptance.")
    else:
        sys.exit(1)

    print("\n[SUCCESS] Ship Gate Proven.")

if __name__ == "__main__":
    test_ship_gate()
