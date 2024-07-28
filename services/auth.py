from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from core.config import SESSION
from core.security import get_password_hash, verify_password
from models import User
from shemas.user import UserCreate


def create_user(db: SESSION, user_info: UserCreate) -> User:
    hashed_password = get_password_hash(user_info.password)
    user_data = user_info.dict()
    user_data['password'] = hashed_password
    user = User(**user_data)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError(statement="Email already registered",
                             params=e.params,
                             orig=e.orig
                             )

    return user


def get_user(db: SESSION, email: EmailStr):
    stmt = select(User).where(User.email == email)
    try:
        user = db.scalars(stmt).one()
    except NoResultFound:
        return None
    return user


def authenticate_user(db: SESSION, email: EmailStr, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

