from vte.db import engine, Base
from vte.orm import Property, Unit
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db_init")

def create_tables():
    logger.info("Connecting to Database and ensuring tables exist...")
    
    # This will create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    logger.info("Tables have been created (if they were missing).")

if __name__ == "__main__":
    create_tables()
