import sys
import os

# Set Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "spine")))

from vte.db import engine, Base
# Import models to register them
from vte.orm import EvidenceBundle, DecisionObject, PermitToken, Property, Unit

def create_tables():
    print("Dropping Tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating Tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables Initialized Successfully.")

if __name__ == "__main__":
    create_tables()
