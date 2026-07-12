from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None


def success_response(message: str, data=None):
    return {
        "success": True,
        "message": message,
        "data": data,
    }