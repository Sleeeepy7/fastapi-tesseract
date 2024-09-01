# from typing import TYPE_CHECKING

# from fastapi import Depends

# from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
# from fastapi_users.authentication import AuthenticationBackend

# from src.config import settings
# from src.database import db_helper
# from src.auth.models import User, AccessToken
# from src.auth.transport import bearer_transport

# if TYPE_CHECKING:
#     from src.auth.models import AccessToken
#     from sqlalchemy.ext.asyncio import AsyncSession


# async def get_user_db(
#     session: "AsyncSession" = Depends(db_helper.session_getter),
# ):
#     yield User.get_db(session=session)


# async def get_access_token_db(
#     session: "AsyncSession" = Depends(db_helper.session_getter),
# ):
#     yield AccessToken.get_db(session=session)


# def get_database_strategy(
#     access_token_db: AccessTokenDatabase["AccessToken"] = Depends(get_access_token_db),
# ) -> DatabaseStrategy:
#     return DatabaseStrategy(
#         database=access_token_db,
#         lifetime_seconds=settings.access_token.lifetime_seconds,
#     )


# auth_backend = AuthenticationBackend(
#     name="access-tokens-db",
#     transport=bearer_transport,
#     get_strategy=get_database_strategy,
# )
