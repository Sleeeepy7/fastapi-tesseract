from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    UserRead,
    UserLogin,
    UserCreate,
    UserRegisterResponse,
    BaseResponse,
    UserLoginResponse,
    UserRegister,
    UserLogoutResponse,
)

from .service import get_by_email, create, get_all_users, get
from .dependencies import check_user_and_get_by_email, get_user_by_id
from .permissions import IsAuthenticatedPermission, PermissionsDependency
from .models import User

from src.database import db_helper
from src.exceptions import CustomHTTPException


auth_router = APIRouter()
user_router = APIRouter()


@user_router.get(
    "",
    response_model=BaseResponse[List[UserRead]],
    dependencies=[
        Depends(
            PermissionsDependency(
                [
                    IsAuthenticatedPermission,
                ]
            )
        ),
    ],
)
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)) -> BaseResponse[List[UserRead]]:
    users = await get_all_users(session=session)

    return BaseResponse(data=users)


@user_router.get("/{user_id}", response_model=BaseResponse[UserRead])
async def get_user(user: User = Depends(get_user_by_id)) -> BaseResponse[UserRead]:
    return BaseResponse(data=user)


@auth_router.post(
    "/register",
    response_model=UserRegisterResponse,
)
async def register_user(
    user_in: UserRegister,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User | CustomHTTPException = Depends(check_user_and_get_by_email),
    response: Response = None,
) -> UserRead | CustomHTTPException:
    user_token = await create(session=session, user_in=user_in)

    response.set_cookie(
        key="Authorization", value=f"Bearer {user_token}", httponly=True, secure=True, samesite="Strict"
    )  # имитируем добавление токена в куки (фронт)

    return UserRegisterResponse(
        data={"token": user_token},
    )


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
)
async def login(
    user_in: UserLogin,
    session: AsyncSession = Depends(db_helper.session_getter),
    response: Response = None,
) -> UserLoginResponse:
    user = await get_by_email(session=session, email=user_in.email)
    if not user:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password.",
        )
    if not user.check_password(password=user_in.password):
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    access_token = user.token
    response.set_cookie(
        key="Authorization", value=f"Bearer {access_token}", httponly=True, secure=True, samesite="Strict"
    )  # имитируем добавление токена в куки (фронт)

    return UserLoginResponse(
        data={"token": access_token},
    )


@auth_router.post("/logout", response_model=UserLogoutResponse)
async def logout(response: Response) -> UserLogoutResponse:
    response.delete_cookie(key="Authorization")
    return UserLogoutResponse(data={"message": "Successfully logged out."})
