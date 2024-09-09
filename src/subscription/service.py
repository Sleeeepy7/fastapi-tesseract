from typing import Optional, List
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

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


async def validate_subscription_purchase(session: AsyncSession, user: User, payment_data: int):
    subscription_plan = await get_subscription_plan_by_id(session, payment_data.plan_id)
    if not subscription_plan or not subscription_plan.is_active:
        raise ValueError("Subscription plan not found or inactive.")

    if not user:
        raise ValueError("User not found.")

    if user.balance < subscription_plan.price:
        raise ValueError("Insufficient funds to purchase a subscription.")

    await session.refresh(user, attribute_names=["active_subscription"])

    if user.active_subscription and user.active_subscription.is_active():
        raise ValueError("The user already has an active subscription.")

    return subscription_plan


async def buy_subscription_plan(session: AsyncSession, user: User, payment_data: int) -> SubscriptionPlan:
    subscription_plan = await validate_subscription_purchase(session, user, payment_data)

    user.balance -= subscription_plan.price

    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=subscription_plan.duration_days)

    new_subscription = UserSubscription(
        user_id=user.id, subscription_plan_id=subscription_plan.id, start_date=start_date, end_date=end_date
    )

    user.active_subscription = new_subscription

    session.add(new_subscription)
    await session.commit()

    return new_subscription


async def get_user_subscription_plan(session: AsyncSession, user: User) -> SubscriptionPlan:
    await session.refresh(user, ["active_subscription"])

    if user.active_subscription:
        await session.refresh(user.active_subscription, ["subscription_plan"])
        return user.active_subscription.subscription_plan

    return None
