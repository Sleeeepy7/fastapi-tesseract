from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserRead, UserRegister, UserLogin, UserCreate, UserRegisterResponse

from .service import get_by_email, create
from .dependencies import check_user_and_get_by_email
from .models import User

from database import db_helper
from exceptions import CustomHTTPException


auth_router = APIRouter()
user_router = APIRouter()


# @user_router.post(
#     "",
#     response_model=UserRead,
# )
# async def create_user(
#     user_in: UserCreate,
#     session: AsyncSession = Depends(db_helper.session_getter),
# ) -> UserRead:
#     user = await get_by_email(session=session, email=user_in.email)
#     if user:
#         print("есть")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="A user with this email already exists.",
#         )

#     user = await create(session=session, user_in=user_in)

#     return user


@auth_router.post(
    "/register",
    response_model=UserRegisterResponse,
)
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User | CustomHTTPException = Depends(check_user_and_get_by_email),
) -> UserRead | CustomHTTPException:
    user_token = await create(session=session, user_in=user_in)

    return UserRegisterResponse(
        data={"token": user_token},
    )
