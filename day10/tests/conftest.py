import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Student


TEST_DATABASE_URL = "sqlite:///./test_students.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

Base.metadata.create_all(bind=test_engine)

# makes FastAPI use the test DB
@pytest.fixture
def override_get_db():
    def _override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    return _override_get_db


"""
Before test
    ↓
Replace get_db with test version
    ↓
Test runs
    ↓
Uses test_students.db
    ↓
After test
    ↓
Clear override
"""

# controls the database schema
@pytest.fixture
def setup_test_database(override_get_db):
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db
    yield

    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()

# controls the database session
@pytest.fixture
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# @pytest.fixture(scope="module")  # Create one client and share it among all tests in this file
@pytest.fixture  # pytest created a new TestClient for each test. That is function scope
def client():
    client = TestClient(app)
    # print(f"Client ID: {id(client)}")
    return client


@pytest.fixture
def test_user():
    return {
        "username": "Samiha",
        "role": "student"
    }


