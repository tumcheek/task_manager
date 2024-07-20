from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import status, Depends
from jwt import InvalidTokenError
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
