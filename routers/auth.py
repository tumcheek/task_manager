from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from core.database import get_db, SESSION
from core.auth import create_access_token, get_current_user
from services.auth import create_user, authenticate_user
from schemas.user import UserCreate, User, Token, UserLogin

router = APIRouter(tags=["users"])


@router.post("/users/")
def register_user(
    user_data: UserCreate, db: Annotated[SESSION, Depends(get_db)]
) -> User:
    """
    Registers a new user in the system.

    Attempts to create a new user in the database using the provided user data.
    If a user with the same email already exists or any other integrity constraint
    is violated, raises an HTTP 400 error.

    Args:
        user_data (UserCreate): The data required to create a new user.
        db (SESSION): The database session dependency.

    Returns:
        User: The newly created user with selected fields (e.g. ID and email).

    Raises:
        HTTPException: If the user cannot be created due to a database integrity error.
    """
    try:
        user = create_user(db, user_data)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.statement)
    return User(id=user.id, email=user.email)


@router.post("/token/")
async def login(user_info: UserLogin, db: Annotated[SESSION, Depends(get_db)]) -> Token:
    """
    Authenticates a user and returns an access token.

    Verifies the user's credentials (email and password). If authentication
    is successful, generates and returns a JWT access token. Otherwise,
    returns an HTTP 401 error with appropriate headers.

    Args:
        user_info (UserLogin): The login credentials including email and password.
        db (SESSION): The database session dependency.

    Returns:
        Token: An access token object containing the JWT and token type.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """
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
    """
    Get the currently authenticated user's profile.

    Returns information about the user associated with the provided access token.
    This endpoint requires authentication via a valid bearer token.

    Args:
        current_user (User): The user extracted from the authentication token,
            resolved through dependency injection.

    Returns:
        User: The authenticated user's profile data.
    """
    return current_user
