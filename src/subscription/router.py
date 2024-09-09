from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.permissions import PermissionsDependency, IsAuthenticatedPermission, IsAdminPermission
from src.database import db_helper
from src.auth.models import User
from src.exceptions import CustomHTTPException
from src.schemas import BaseResponse
from src.auth.dependencies import get_current_user

from .schemas import SubscriptionPlanResponse, SubscriptionPlanCreate, SubscriptionPlanRead, SubscriptionPurchase
from .service import (
    create_subscription_plan,
    get_subscription_plan_list,
    get_user_subscription_plan,
    get_subscription_plan_by_id,
    buy_subscription_plan,
)


subscription_router = APIRouter()


# @subscription_router.get(
#     "",
#     dependencies=[
#         Depends(
#             PermissionsDependency(
#                 [
#                     IsAuthenticatedPermission,
#                 ]
#             )
#         ),
#     ],
# )
# async def test():
#     return {"test"}


@subscription_router.post(
    "/create",
    dependencies=[
        Depends(
            PermissionsDependency(
                [
                    IsAuthenticatedPermission,
                    IsAdminPermission,
                ]
            )
        )
    ],
    response_model=SubscriptionPlanResponse,
)
async def create_sub_plan(
    sub_plan_in: SubscriptionPlanCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sub_plan = await create_subscription_plan(session, sub_plan_in)
    return SubscriptionPlanResponse(data=sub_plan)


@subscription_router.get("", response_model=BaseResponse[list[SubscriptionPlanRead]])
async def get_sub_plans(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sub_plans = await get_subscription_plan_list(session)
    if not sub_plans:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription plans are not available yet.",
        )
    return BaseResponse(data=sub_plans)


@subscription_router.get("/{plan_id}", response_model=SubscriptionPlanResponse)
async def get_sub_plan_by_id(
    plan_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sub_plan = await get_subscription_plan_by_id(session, plan_id)

    if not sub_plan:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription plan not found.",
        )

    return SubscriptionPlanResponse(data=sub_plan)


@subscription_router.post("/buy", response_model=SubscriptionPlanResponse)  # TODO: поменял с плана на подписку
async def buy_sub_plan_by_id(
    payment_data: SubscriptionPurchase,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        subscription_data = await buy_subscription_plan(session, current_user, payment_data)

        if not subscription_data:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to purchase subscription plan.",
            )

        return SubscriptionPlanResponse(data=subscription_data)
    except ValueError as e:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@subscription_router.get("/me", response_model=SubscriptionPlanResponse)
async def get_me(
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    sub_plan = await get_user_subscription_plan(session, current_user)

    if not sub_plan:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User subscription plan not found.",
        )

    return SubscriptionPlanResponse(data=sub_plan)  # TODO: поменял с плана на подписку
