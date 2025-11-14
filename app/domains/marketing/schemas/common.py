"""Common schemas for marketing domain."""
from pydantic import BaseModel
from typing import TypeVar, Generic, List

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
