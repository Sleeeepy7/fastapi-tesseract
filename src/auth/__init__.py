from fastapi import APIRouter

from src.auth.router import auth_router
from src.auth.router import user_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["authentication"])
router.include_router(user_router, prefix="/users", tags=["users"])
