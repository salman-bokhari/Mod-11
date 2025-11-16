import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base

# Get DATABASE_URL from env (should be set in GH Actions)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Setup engine with timeout to avoid hangs
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {},
    pool_pre_ping=True,
    connect_args={'connect_timeout': 5} if not DATABASE_URL.startswith('sqlite') else {}
)

SessionTesting = sessionmaker(bind=engine)

# Create tables for tests
Base.metadata.create_all(bind=engine)

# Fixture for DB session
@pytest.fixture(scope="function")
def db_session():
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()

# Fixture for FastAPI test client
@pytest.fixture(scope="function")
def client(db_session):
    # Override get_db to use test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
