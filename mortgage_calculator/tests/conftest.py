import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db

# SQLite database URL for testing
SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


# Fixture to generate a user payload
@pytest.fixture(scope="function")
def property_payload():
    """Generate a property payload."""
    return {
        "purchase_price": 300000,
        "rental_income": 2500,
        "renovation_cost": 50000,
        "property_name": "123 Elm Steet",
        "admin_costs": 3000,
        "management_fees": 200,
    }


@pytest.fixture
def update_property_payload():
    """Generate an updated property payload."""
    return {
        "rental_income": 4000,
        "property_name": "456 Elm Street",
    }


@pytest.fixture(scope="function")
def mortgage_payload():
    """Generate a mortgage payload."""
    return {
        "loan_to_value": 100,
        "interest_rate": 3,
        "mortgage_type": "repayment",
        "loan_term": 30,
    }


@pytest.fixture(scope="function")
def update_mortgage_payload():
    """Generate an updated mortgage payload."""
    return {
        "interest_rate": 2.5,
    }
