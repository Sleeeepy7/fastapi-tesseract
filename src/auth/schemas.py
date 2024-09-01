from typing import Optional, Dict, Any

from pydantic import EmailStr, Field

from schemas import ProjectBase, BaseResponse


class UserBase(ProjectBase):
    email: EmailStr


class UserRead(UserBase):
    id: int


class UserLogin(UserBase):
    password: str


class UserRegister(UserLogin):
    pass


class UserCreate(UserLogin):
    pass


class UserTokenData(ProjectBase):
    token: str


class UserRegisterResponse(BaseResponse[UserTokenData]):
    pass
