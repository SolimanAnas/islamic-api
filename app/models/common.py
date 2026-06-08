from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int


class APIResponse(BaseModel):
    success: bool = True
    data: Any = None
    message: str | None = None


class PaginatedResponse(BaseModel):
    success: bool = True
    data: list[Any] = []
    meta: PaginationMeta
