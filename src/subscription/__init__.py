from fastapi import APIRouter

from src.subscription.router import subscription_router

router = APIRouter()

router.include_router(subscription_router, prefix="/subscription", tags=["subscription"])
