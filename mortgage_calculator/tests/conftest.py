import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError

from app.database import Base, get_db
from app.main import app


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",  # For Postgres use "postgresql://user:password@localhost/dbname"
        action="store",
        default="sqlite:///./test_db.db",  # Default uses SQLite in memory db
        help="Database URL to use for tests.",
    )


# @pytest.hookimpl(tryfirst=True)
# def pytest_sessionstart(session):
#     db_url = session.config.getoption("--dburl")
#     try:
#         # Attempt to create an engine and connect to the database.
#         engine = create_engine(
#             db_url,
#             connect_args={"check_same_thread": False} if "sqlite" in db_url else {},
#         )
#         connection = engine.connect()
#         connection.close()  # Close the connection right after a successful connect.
#         print("Database connection successful........")
#     except SQLAlchemyOperationalError as e:
#         print(f"Failed to connect to the database at {db_url}: {e}")
#         pytest.exit(
#             "Stopping tests because database connection could not be established."
#         )


@pytest.fixture(scope="session")
def db_url(request):
    """Fixture to retrieve the database URL."""
    return request.config.getoption("--dburl")


@pytest.fixture(scope="function")
def db_session(db_url):
    """Create a new database session with a rollback at the end of the test."""
    # Create a SQLAlchemy engine
    engine = create_engine(
        db_url,
        poolclass=StaticPool,
    )

    # Create a sessionmaker to manage sessions
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables in the database
    Base.metadata.create_all(bind=engine)
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


@pytest.fixture(scope="function")
def property_endpoint():
    return "/api/v1/property/"


@pytest.fixture(scope="function")
def mortgage_endpoint():
    return "/api/v1/mortgage/"


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
