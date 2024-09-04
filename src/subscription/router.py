from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.permissions import PermissionsDependency, IsAuthenticatedPermission, IsAdminPermission
from src.database import db_helper
from src.auth.models import User
from src.exceptions import CustomHTTPException
from src.schemas import BaseResponse
from src.auth.dependencies import get_current_user

from .schemas import SubscriptionPlanResponse, SubscriptionPlanCreate, SubscriptionPlanRead
from .service import create_subscription_plan, get_subscription_plan_list


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


@subscription_router.get("/me")
async def test_router(
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    print("################################")
    print(current_user)
    print(current_user.email)
