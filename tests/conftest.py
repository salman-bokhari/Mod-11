import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Build connect_args safely
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    connect_args["connect_timeout"] = 5

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionTesting = sessionmaker(bind=engine)

# For sqlite local tests, create tables here; for CI with Postgres, tests can create/drop
if DATABASE_URL.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    # override dependency so API uses our test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # cleanup override
    app.dependency_overrides.pop(get_db, None)
