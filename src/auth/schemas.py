from typing import Optional, Dict, Any, List

from pydantic import EmailStr, Field, field_validator

from .utils import hash_password

from schemas import ProjectBase, BaseResponse


class UserBase(ProjectBase):
    email: EmailStr


class UserRead(UserBase):
    id: int


class UserLogin(UserBase):
    password: str


class UserRegister(UserLogin):
    pass

    @field_validator("password", mode="before")
    def hash_password(cls, v):
        return hash_password(str(v))


class UserCreate(UserLogin):
    pass

    @field_validator("password", mode="before")
    def hash_password(cls, v):
        return hash_password(str(v))


class UserTokenData(ProjectBase):
    token: str


class UserRegisterResponse(BaseResponse[UserTokenData]):
    pass


class UserLoginResponse(BaseResponse[UserTokenData]):
    pass


class UserLogoutResponse(BaseResponse[dict]):
    pass
