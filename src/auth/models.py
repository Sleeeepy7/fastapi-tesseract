import secrets
from typing import TYPE_CHECKING

from src.models import Base
from src.mixins import PrimaryKeyMixin, TimeStampMixin

import bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String, LargeBinary, Boolean, event, Float


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.subscription.models import UserSubscription


class User(Base, PrimaryKeyMixin, TimeStampMixin):
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    token: Mapped[str | None] = mapped_column(String, nullable=True)
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    # ссылка на активную подписку (id)
    active_subscription_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("user_subscriptions.id"), nullable=True)

    # # ссылка на активную подписку (ссылка на сам обьект активной подписки (некий орм))
    active_subscription: Mapped["UserSubscription"] = relationship(
        "UserSubscription", foreign_keys=[active_subscription_id], uselist=False
    )

    # связь с историей подписок
    subscriptions: Mapped["UserSubscription"] = relationship("UserSubscription", back_populates="user")

    # связь с историей платежей
    # payments: Mapped[""] = relationship("PaymentHistory", back_populates="user")

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
