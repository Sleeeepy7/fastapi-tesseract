from abc import ABC, abstractmethod

from fastapi import Depends, Request, status

from sqlalchemy.ext.asyncio import AsyncSession

from .service import get_by_token

from src.database import db_helper
from src.exceptions import CustomHTTPException


async def get_user_from_token(token: str, session: AsyncSession):
    try:
        user = await get_by_token(session, token)
        if user is None:
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return user
    except Exception as e:
        print(e)
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


class BasePermission(ABC):
    """Абстрактный класс для проверки разрешений."""

    @abstractmethod
    def has_required_permissions(self, request: Request, user: dict) -> bool:
        """Метод для определения конкретных разрешений."""
        pass

    async def init_permission(self, request: Request, session: AsyncSession):
        """Асинхронная инициализация разрешений."""
        # Поиск в заголовке
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            # Поиск в куках
            auth_cookie = request.cookies.get("Authorization")
            if auth_cookie:
                auth_header = auth_cookie

        if not auth_header or not auth_header.startswith("Bearer "):
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
            )

        token = auth_header.split(" ")[1]

        user = await get_user_from_token(session=session, token=token)

        if not self.has_required_permissions(request, user):
            raise CustomHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )


class IsAuthenticatedPermission(BasePermission):
    """Проверяет, авторизован ли пользователь."""

    def has_required_permissions(self, request: Request, user: dict) -> bool:
        return user is not None


class PermissionsDependency:
    """Зависимость для проверки разрешений."""

    def __init__(self, permission_classes: list):
        self.permission_classes = permission_classes

    async def __call__(self, request: Request, session: AsyncSession = Depends(db_helper.session_getter)):
        for permission_class in self.permission_classes:
            permission_instance = permission_class()
            await permission_instance.init_permission(request=request, session=session)
