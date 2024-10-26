from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from core.database import get_db, SESSION
from core.auth import create_access_token, get_current_user
from services.auth import create_user, authenticate_user
from schemas.user import UserCreate, User, Token, UserLogin

router = APIRouter(tags=['users'])


@router.post('/users/')
def register_user(user_data: UserCreate, db: Annotated[SESSION, Depends(get_db)]) -> User:
    try:
        user = create_user(db, user_data)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.statement)
    return User(id=user.id, email=user.email)


@router.post("/token/")
async def login(user_info: UserLogin, db: Annotated[SESSION, Depends(get_db)]) -> Token:
    user = authenticate_user(db, user_info.email, user_info.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
