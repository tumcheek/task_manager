import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from core.config import TEST_DATABASE_URL
from core.database import get_db
from main import app
from models import Base, User, Task


@pytest.fixture(scope="session")
def engine():
    """Create a new SQLAlchemy engine for testing."""
    return create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture(scope="session")
def tables(engine):
    """Create all tables before the tests run, and drop them after."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def dbsession(engine, tables):
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def user(dbsession):
    """Create a user for testing."""
    user = User(
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        password="Testpassword",
    )
    dbsession.add(user)
    dbsession.commit()
    return user


@pytest.fixture
def another_user(dbsession):
    """Create a user for testing."""
    user = User(
        first_name="Test",
        last_name="User",
        email="anothertestuser@example.com",
        password="Testpassword",
    )
    dbsession.add(user)
    dbsession.commit()
    return user


@pytest.fixture
def user_task(dbsession, user):
    """Create a task for testing."""
    task = Task(
        title="Test Task",
        description="Task for testing",
        owner_id=user.id,
    )

    dbsession.add(task)
    dbsession.commit()
    dbsession.refresh(task)
    return task


@pytest.fixture
def another_user_task(dbsession, another_user):
    """Create a task for testing."""
    task = Task(
        title="Another User's Task",
        description="This task belongs to another user.",
        owner_id=another_user.id,
    )
    dbsession.add(task)
    dbsession.commit()
    dbsession.refresh(task)
    return task


@pytest.fixture
def client(dbsession):
    """Creates a FastAPI test client with overridden dependencies."""

    def override_get_db():
        try:
            yield dbsession
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def task_detail_url():
    return "/api/v1/tasks/{task_id}/"
