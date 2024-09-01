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
