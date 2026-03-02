import sys
print("Step 1: Importing config")
import vte.db
print("Step 2: Engine created")
import vte.orm
print("Step 3: ORM registered")
from vte.db import engine, Base
print("Step 4: About to drop_all")
Base.metadata.drop_all(bind=engine)
print("Step 5: About to create_all")
Base.metadata.create_all(bind=engine)
print("Step 6: Done")
