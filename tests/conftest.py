import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import TEST_DATABASE_URL
from models import Base, User


@pytest.fixture(scope='session')
def engine():
    """Create a new SQLAlchemy engine for testing."""
    return create_engine(TEST_DATABASE_URL)


@pytest.fixture(scope='session')
def tables(engine):
    """Create all tables before the tests run, and drop them after."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
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
    user = User(first_name='Test', last_name='User', email='testuser@example.com', password='Testpassword')
    dbsession.add(user)
    dbsession.commit()
    return user

