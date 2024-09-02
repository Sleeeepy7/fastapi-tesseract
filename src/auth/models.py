import secrets
from typing import TYPE_CHECKING

from models import Base
from mixins import PrimaryKeyMixin, TimeStampMixin

import bcrypt
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, String, LargeBinary, Boolean, event


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


class User(Base, PrimaryKeyMixin, TimeStampMixin):
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    token: Mapped[str | None] = mapped_column(String, nullable=True)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @staticmethod
    def generate_token() -> str:
        return secrets.token_hex(32)  # генерация токена

    @classmethod
    def __declare_last__(cls):
        super().__declare_last__()
        event.listen(cls, "before_insert", cls._generate_token)

    @staticmethod
    def _generate_token(mapper, connection, target):
        if not target.token:
            target.token = User.generate_token()
