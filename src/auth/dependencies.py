from fastapi import Depends, HTTPException, status, Request

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .models import User
from .schemas import UserCreate
from .service import get_by_email, get, get_user_by_token


from src.exceptions import CustomHTTPException
from src.database import db_helper


async def get_current_user(request: Request, session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    try:
        auth_header = request.cookies.get("Authorization")
        auth_token = auth_header.split(" ")[1]

        if not auth_token or not auth_header.startswith("Bearer "):
            raise CustomHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token was not provided")

        user = await get_user_by_token(session, auth_token)

        if not user:
            raise CustomHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")

        return user
    except Exception:
        raise CustomHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token was not provided.")


async def check_user_and_get_by_email(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    user = await get_by_email(session=session, email=user_in.email)
    if user:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    return user


async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    user = await get(session=session, user_id=user_id)
    if not user:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
