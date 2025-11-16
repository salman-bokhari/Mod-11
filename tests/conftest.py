import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base

# DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Prepare connect_args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    connect_args["connect_timeout"] = 5

# Engine setup
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionTesting = sessionmaker(bind=engine)

# Create tables (for SQLite)
if DATABASE_URL.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

# Fixture for DB session
@pytest.fixture(scope="function")
def db_session():
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()

# Fixture for FastAPI client
@pytest.fixture(scope="function")
def client(db_session):
    # Override get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
