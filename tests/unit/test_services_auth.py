import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import User
from schemas.user import UserCreate
from services.auth import create_user


def test_create_user_success(dbsession, mocker):
    """Test that a user can be successfully created."""
    user_info = UserCreate(email='test@example.com', password='password123', first_name='test', last_name='test')
    hashed_password = 'hashed_password123'
    mocker.patch('services.auth.get_password_hash', return_value=hashed_password)

    user = create_user(dbsession, user_info)

    assert user.id is not None
    assert user.email == 'test@example.com'
    assert user.password == hashed_password
    user_in_db = dbsession.query(User).filter_by(email='test@example.com').one()
    assert user_in_db == user


def test_create_user_duplicate_email(dbsession, mocker):
    """Test that creating a user with an existing email raises an IntegrityError."""
    user_info = UserCreate(email='duplicate@example.com', password='password123', first_name='test', last_name='test')
    hashed_password = 'hashed_password123'
    mocker.patch('core.security.get_password_hash', return_value=hashed_password)
    create_user(dbsession, user_info)

    with pytest.raises(IntegrityError) as exc_info:
        create_user(dbsession, user_info)

    assert 'Email already registered' in str(exc_info.value)


def test_user_create_password_too_short():
    """Test that creating a user with a short password raises ValidationError."""
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'short'
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**user_data)

    errors = exc_info.value.errors()
    assert any(
        error['loc'] == ('password',) and
        error['msg'] == 'String should have at least 8 characters'
        for error in errors
    )
