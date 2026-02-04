from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Configuration (Env vars with defaults for DEV)
# In production, these MUST be provided by the environment.
DB_USER = os.getenv("POSTGRES_USER", "spine_app")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "dev_only_password_123")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "vte_spine")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DATABASE_URL = "sqlite:///./vte_spine.db"

# Create Engine
# pool_pre_ping=True handles DB connection drops gracefully
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def get_db():
    """Dependency for FastAPI Routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
