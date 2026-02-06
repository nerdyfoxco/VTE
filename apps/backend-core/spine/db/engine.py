from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Real World: Use ENV var for DB URL. Fallback to sqlite for dev ONLY if not set.
# In Production, this env var IS MANDATORY.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vte_backend.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
