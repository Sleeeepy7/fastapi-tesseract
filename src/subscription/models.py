import secrets
from typing import TYPE_CHECKING
from datetime import datetime

from src.models import Base
from src.mixins import PrimaryKeyMixin, TimeStampMixin

import bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String, LargeBinary, Boolean, event, Float, DateTime


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.auth.models import User


class SubscriptionPlan(Base, PrimaryKeyMixin):
    __tablename__ = "subscription_plans"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)  # кол-во дней подписки
    price: Mapped[float] = mapped_column(Float, nullable=False)  # цена подписки
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # активен ли конкретный план подписки


class UserSubscription(Base, PrimaryKeyMixin, TimeStampMixin):
    __tablename__ = "user_subscriptions"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscription_plans.id"), nullable=False)

    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # когда подписка началась
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # когда подписка истекает

    # связь с пользователем и планом подписки
    user: Mapped["User"] = relationship("User", back_populates="subscriptions", foreign_keys=[user_id])
    subscription_plan: Mapped["SubscriptionPlan"] = relationship("SubscriptionPlan")

    def is_active(self) -> bool:
        return self.end_date >= datetime.utcnow()


# class PaymentHistory(Base, PrimaryKeyMixin, TimeStampMixin):
#     __tablename__ = 'payment_history'

#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
#     subscription_plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscription_plans.id"), nullable=False)

#     payment_amount: Mapped[float] = mapped_column(Float, nullable=False)
#     payment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
#     payment_method: Mapped[str] = mapped_column(String, nullable=False)  # метод оплаты

#     user = relationship("User", back_populates="payments")
#     subscription_plan = relationship("SubscriptionPlan")
