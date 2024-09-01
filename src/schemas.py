from datetime import datetime
from typing import Generic, TypeVar, Optional, Any, List

from pydantic import BaseModel, SecretStr

T = TypeVar("T")


class ProjectBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }


class BaseResponse(BaseModel, Generic[T]):
    status: bool = True
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    status: bool = False
    error: str
    details: Optional[List[Any]] = None
