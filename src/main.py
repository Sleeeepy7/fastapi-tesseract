from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.database import db_helper

from src.exceptions import CustomHTTPException, custom_http_exception_handler
from src.auth import router as auth_router
from src.subscription import router as subscription_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    root_path="/api/v1",
    # responses={
    #     400: {"model": ErrorResponse, "description": "Bad Request"},
    #     422: {"model": ErrorResponse, "description": "Validation Error"},
    #     500: {"model": ErrorResponse, "description": "Internal Server Error"},
    # },
)

# main_app.add_middleware(ExceptionMiddleware)
# main_app.add_exception_handler(RequestValidationError, validation_exception_handler)
main_app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)

main_app.include_router(auth_router)
main_app.include_router(subscription_router)

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:main_app",
#         host=settings.run.host,
#         port=settings.run.port,
#         reload=True,
#     )
