from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    page: int
    limit: int
    results: List[T]
