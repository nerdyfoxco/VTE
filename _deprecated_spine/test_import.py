import sys
print("Starting import test...")
try:
    print("Importing main app...")
    import vte.main
    print("Successfully imported vte.main")
except Exception as e:
    import traceback
    traceback.print_exc()
