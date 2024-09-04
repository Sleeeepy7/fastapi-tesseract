from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import User
from .schemas import UserCreate, UserRegister


async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
    result = await session.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    return user


async def create(session: AsyncSession, user_in: (UserCreate | UserRegister)) -> str:
    password = bytes(user_in.password, "utf-8")
    user = User(**user_in.model_dump(exclude={"password"}), password=password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user.token


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return list(users)


async def get(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    return user


async def get_by_token(session: AsyncSession, token: str) -> Optional[User]:
    result = await session.execute(select(User).filter(User.token == token))
    user = result.scalars().first()
    return user


async def get_user_by_token(session: AsyncSession, auth_token: str) -> Optional[User]:
    user = await session.execute(select(User).where(User.token == auth_token))
    user = user.scalars().first()
    return user
