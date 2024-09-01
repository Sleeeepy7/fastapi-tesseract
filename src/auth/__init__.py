from fastapi import APIRouter

from auth.router import auth_router
from auth.router import user_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["authentication"])
router.include_router(user_router, prefix="/users", tags=["users"])
