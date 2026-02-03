
import uvicorn
import sys
import os


# Ensure path is correct
sys.path.insert(0, os.path.abspath("apps/backend-core"))

# Force SQLite for Local Verification (Overrides .env)
os.environ["DATABASE_URL"] = "sqlite:///./vte_spine.db"

print("Importing dependencies manually...")
try:
    print("  Importing config...")
    import spine.config
    print("  config OK")
    print("  Importing secrets...")
    import spine.ops.secrets
    print("  secrets OK")
    print("  Importing db.session...")
    import spine.db.session
    print("  db.session OK")
    print("Dependencies OK")
except Exception as e:
    print(f"Dependency FAIL: {e}")
    sys.exit(1)

print("Importing spine.main:app...")
try:
    from spine.main import app
    print("Import Successful.")
except Exception as e:
    print(f"CRITICAL IMPORT ERROR: {e}")
    sys.exit(1)

import time

if __name__ == "__main__":
    print("Starting Uvicorn for Spine...")
    try:
        print("Starting uvicorn.run on 0.0.0.0:8003...")
        uvicorn.run(app, host="0.0.0.0", port=8003, log_level="debug")
        print("Uvicorn returned control. Sleeping...")
        time.sleep(30)
    except Exception as e:
        print(f"CRITICAL RUNTIME ERROR: {e}")
