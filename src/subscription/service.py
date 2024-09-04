from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .schemas import SubscriptionPlanCreate, SubscriptionPlanRead
from .models import SubscriptionPlan, UserSubscription

from src.auth.models import User


async def create_subscription_plan(session: AsyncSession, sub_plan_in: SubscriptionPlanCreate) -> SubscriptionPlan:
    new_plan = SubscriptionPlan(**sub_plan_in.model_dump())
    session.add(new_plan)
    await session.commit()

    return new_plan


async def get_subscription_plan_list(session: AsyncSession) -> Optional[List[SubscriptionPlan]]:
    result = await session.execute(select(SubscriptionPlan).order_by(SubscriptionPlan.id))
    sub_plans = result.scalars().all()
    return list(sub_plans)


async def get_subscription_plan_by_id(session: AsyncSession, subscription_id: int) -> SubscriptionPlan:
    result = await session.execute(select(SubscriptionPlan).filter(SubscriptionPlan.id == subscription_id))
    sub_plan = result.scalars().first()
    return sub_plan


async def buy_subscription_plan(session: AsyncSession, user: User, subscription_plan_id: int) -> SubscriptionPlan:
    subscription_plan = await get_subscription_plan_by_id(session, subscription_plan_id)
    if not subscription_plan or not subscription_plan.is_active:
        pass
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription plan not found or inactive.")

    pass
