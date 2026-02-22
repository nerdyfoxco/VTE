import pytest
from vte.db import engine, Base

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    print("Creating Database Tables...")
    Base.metadata.create_all(bind=engine)
    yield
    print("Teardown (Keeping DB for inspection)")
