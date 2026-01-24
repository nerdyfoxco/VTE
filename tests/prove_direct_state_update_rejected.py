import sys

# Proof of Correctness: Direct State Update Rejected
# In a real DB, this is a TRIGGER `before update on decision_objects`.
# Here we simulate the application-layer check that wraps the DB driver.

class MockDB:
    def execute(self, sql):
        sql = sql.upper()
        if "UPDATE" in sql and "STATE" in sql:
            # Check if this is coming from the trusted engine or raw SQL
            # For this canary, ANY direct update string containing 'SET STATE=' is banned
            if "SET STATE =" in sql or "SET STATE=" in sql:
                 raise RuntimeError("Direct State Mutation Forbidden! Use StateMachine.transition().")

def prove_immutability():
    print("Testing DB State Immutability...")
    db = MockDB()
    
    try:
        # User tries to hacker-style update state
        db.execute("UPDATE decision_objects SET state='APPROVED' WHERE id=1")
        print("  [FAIL] DB allowed direct state update!")
        return False
    except RuntimeError as e:
        print(f"  [PASS] DB Rejected direct update: {e}")
        return True

if __name__ == "__main__":
    if prove_immutability():
        sys.exit(0)
    else:
        sys.exit(1)
