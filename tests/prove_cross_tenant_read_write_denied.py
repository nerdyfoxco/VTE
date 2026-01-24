import sys
import sqlite3

# Proof: Cross-Tenant Access Denied
# Simulates RLS (Row Level Security) enforcement.

class MockRLSDB:
    def __init__(self):
        self.current_tenant = None
        self.data = {
            "tenant_A": ["secret_A1", "secret_A2"],
            "tenant_B": ["secret_B1"]
        }
        
    def set_session_tenant(self, tenant_id):
        print(f"  [DB] Setting Session Tenant to: {tenant_id}")
        self.current_tenant = tenant_id
        
    def select_all_secrets(self):
        # Simulates: SELECT * FROM secrets;
        # RLS Filter: WHERE tenant_id = current_tenant
        if not self.current_tenant:
             raise PermissionError("No Tenant Context set!")
             
        # Return only data for current tenant
        return self.data.get(self.current_tenant, [])
        
    def direct_insert_attempt(self, target_tenant, value):
        # Simulates: INSERT INTO secrets (tenant_id, val) VALUES ...
        # RLS Check: NEW.tenant_id must match current_tenant
        if target_tenant != self.current_tenant:
             raise PermissionError(f"RLS Violation: Cannot insert for {target_tenant} while scoped to {self.current_tenant}")
        self.data.setdefault(target_tenant, []).append(value)
        return True

def prove_isolation():
    print("Testing Tenant Isolation (RLS Simulation)...")
    db = MockRLSDB()
    
    # 1. Test Read Isolation
    db.set_session_tenant("tenant_A")
    results = db.select_all_secrets()
    print(f"  Tenant A sees: {results}")
    
    if "secret_B1" in results:
        print("  [FAIL] Tenant A saw Tenant B's data!")
        return False
        
    if "secret_A1" not in results:
        print("  [FAIL] Tenant A could not see own data.")
        return False
        
    print("  [PASS] Read Isolation Verified.")
    
    # 2. Test Write Isolation (Cross-Tenant Write)
    print("  Attempting Cross-Tenant Write (A writing to B)...")
    try:
        db.direct_insert_attempt("tenant_B", "malicious_entry")
        print("  [FAIL] Writer allowed cross-tenant insert!")
        return False
    except PermissionError as e:
        print(f"  [PASS] Write blocked: {e}")
        
    return True

if __name__ == "__main__":
    if prove_isolation():
        sys.exit(0)
    else:
        sys.exit(1)
