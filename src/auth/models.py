from typing import TYPE_CHECKING

from src.models import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey

# from fastapi_users_db_sqlalchemy import (
#     SQLAlchemyBaseUserTable,
#     SQLAlchemyUserDatabase,
# )
# from fastapi_users_db_sqlalchemy.access_token import (
#     SQLAlchemyAccessTokenDatabase,
#     SQLAlchemyBaseAccessTokenTable,
# )

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base):
    pass
    # @classmethod
    # def get_db(cls, session: "AsyncSession"):
    #     return SQLAlchemyUserDatabase(session, User)


# class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
#     user_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#     )

#     @classmethod
#     def get_db(cls, session: "AsyncSession"):
#         return SQLAlchemyAccessTokenDatabase(session, AccessToken)
