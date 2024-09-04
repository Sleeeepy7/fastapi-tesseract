from typing import Optional, Dict, Any, List

from pydantic import EmailStr, Field, field_validator

from src.schemas import ProjectBase, BaseResponse


class PlanBase(ProjectBase):
    name: str
    description: str | None = None
    duration_days: int
    price: float


class SubscriptionPlanRead(PlanBase):
    id: int


class SubscriptionPlanCreate(PlanBase):
    is_active: bool = True

    @field_validator("duration_days")
    def duration_must_be_at_least_one_day(cls, value):
        if value < 1:
            raise ValueError("Subscription duration must be at least one day")
        return value

    # Проверка, что цена не меньше 0
    @field_validator("price")
    def price_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError("Price must be positive")
        return value


class SubscriptionPlanResponse(BaseResponse[SubscriptionPlanRead]):
    pass
