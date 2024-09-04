# from starlette.middleware.base import BaseHTTPMiddleware

# from fastapi import Request, status
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError

# from pydantic import ValidationError

# import logging

# log = logging.getLogger(__name__)


# class ExceptionMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         try:
#             response = await call_next(request)
#         except RequestValidationError as e:  # Обработка валидационных ошибок
#             log.exception(e)
#             response = JSONResponse(
#                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 content={
#                     "status": False,
#                     "error": "Validation error",
#                     "details": e.errors(),
#                 },
#             )
#         except ValidationError as e:  # Обработка ошибок валидации Pydantic
#             log.exception(e)
#             response = JSONResponse(
#                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 content={
#                     "status": False,
#                     "error": "Validation error",
#                     "details": e.errors(),
#                 },
#             )
#         except Exception as e:  # Обработка всех других ошибок
#             log.exception(e)
#             response = JSONResponse(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 content={
#                     "status": False,
#                     "error": "An unexpected error occurred.",
#                     "details": {},
#                 },
#             )
#         return response
