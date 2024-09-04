from typing import Any, Optional, List

from fastapi import Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import logging

log = logging.getLogger(__name__)


# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     log.exception(exc)
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "status": False,
#             "error": "Validation error",
#             "details": exc.errors(),
#         },
#     )


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, details: Optional[List[Any]] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.details = details

    def to_response(self):
        return {
            "status": False,
            "error": self.detail,
            "details": self.details or [],
        }


async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response(),
    )
