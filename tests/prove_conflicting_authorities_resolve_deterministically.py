import json
import os
import sys

# Contract paths
AUTHORITY_CHAIN_PATH = "contracts/authority_chain.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class AuthorityArbiter:
    def __init__(self, chain_contract):
        # Sort by level ASC (Lower level wins)
        self.hierarchy = sorted(
            chain_contract['hierarchy'], 
            key=lambda x: x['level']
        )
        
    def resolve(self, requested_action, claims):
        # claims = list of (role, vote)
        # vote = ALLOW or DENY
        
        print(f"  > Resolving claims for action: {requested_action}")
        
        # Iterate hierarchy levels (0 is highest authority)
        for node in self.hierarchy:
            role = node['role']
            # Start form top
            # If a role has an opinion, that opinion WINS if it conflicts with lower levels?
            # Actually, "LOWER_LEVEL_WINS" usually means Level 0 > Level 1.
            # Let's check claims for this role.
            
            for claim_role, claim_vote in claims:
                if claim_role == role:
                    print(f"    - Match at Level {node['level']} ({role}): {claim_vote}")
                    return claim_vote
                    
        return "DEFAULT_DENY" # Fallback

def test_authority_resolution():
    print("[INFO] Loading Authority Chain...")
    contract = load_json(AUTHORITY_CHAIN_PATH)
    arbiter = AuthorityArbiter(contract)
    
    # Scenario: User wants to change Email (Allowed), but Legal Hold (Deny)
    claims = [
        ("CUSTOMER_PREFERENCE", "ALLOW"),
        ("LEGAL_HOLD_POLICY", "DENY")
    ]
    
    # Legal Hold is Level 0, Customer is Level 5.
    # Level 0 should be checked first and win.
    
    result = arbiter.resolve("ChangeEmail", claims)
    if result != "DENY":
        print(f"[FAIL] Legal Hold (Level 0) failed to override Customer (Level 5)! Result: {result}")
        sys.exit(1)
        
    print("[PASS] Legal Hold correctly blocked the action.")

    # Scenario 2: Business Logic vs Customer
    claims2 = [
        ("DEFAULT_BUSINESS_LOGIC", "DENY"), # Level 10
        ("CUSTOMER_PREFERENCE", "ALLOW")    # Level 5
    ]
    result2 = arbiter.resolve("OptOut", claims2)
    if result2 != "ALLOW":
         print(f"[FAIL] Customer (Level 5) failed to override Business Logic (Level 10)! Result: {result2}")
         sys.exit(1)
         
    print("[PASS] Customer Preference correctly overrode default logic.")

def main():
    try:
        test_authority_resolution()
        print("\n[SUCCESS] Authority Chain Resolution Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
