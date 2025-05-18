from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from models import User
from schemas.user import UserCreate


def create_user(db: Session, user_info: UserCreate) -> User:
    hashed_password = get_password_hash(user_info.password)
    user_data = user_info.dict()
    user_data["password"] = hashed_password
    user = User(**user_data)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError(
            statement="Email already registered", params=e.params, orig=e.orig
        )

    return user


def get_user(db: Session, email: EmailStr):
    stmt = select(User).where(User.email == email)
    try:
        user = db.scalars(stmt).one()
    except NoResultFound:
        return None
    return user


def authenticate_user(db: Session, email: EmailStr, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
