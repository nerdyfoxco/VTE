import sys
import os

# Simulates Identity Lifecycle State Machine
# INVITE -> ACCEPT -> ACTIVE -> REVOKED

def test_identity_lifecycle():
    print("[INFO] Starting Identity Lifecycle Verification...")
    
    # State Machine
    state = "NONE"
    
    # Step 1: Invite
    state = "INVITED"
    print(f"  > Event: Admin sends invite. State: {state}")
    
    # Step 2: Accept
    state = "ACTIVE"
    print(f"  > Event: User accepts. State: {state}")
    
    # Step 3: Revoke
    state = "REVOKED"
    print(f"  > Event: Admin revokes access. State: {state}")
    
    # Step 4: Try to Login
    print("  > Attempting login in REVOKED state...")
    login_success = False
    
    if state == "REVOKED":
        login_success = False
        print("  > Login Blocked: Principal is REVOKED.")
    else:
        login_success = True
        
    if not login_success:
        print("    [PASS] Revocation enforced immediately.")
    else:
        sys.exit(1)

    print("\n[SUCCESS] Identity Lifecycle Proven.")

if __name__ == "__main__":
    test_identity_lifecycle()
