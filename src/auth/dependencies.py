from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_helper

from .models import User
from .schemas import UserCreate
from .service import get_by_email


from exceptions import CustomHTTPException


async def check_user_and_get_by_email(user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    user = await get_by_email(session=session, email=user_in.email)
    if user:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    return user
