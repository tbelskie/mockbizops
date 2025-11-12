"""Utility functions."""
from typing import List, TypeVar, Generic
from sqlalchemy.orm import Query
from app.schemas.common import PaginatedResponse
from app.config import settings
import math

T = TypeVar("T")


def paginate(
    query: Query,
    page: int = 1,
    page_size: int = None
) -> tuple:
    """
    Paginate a SQLAlchemy query.

    Args:
        query: SQLAlchemy query to paginate
        page: Page number (1-indexed)
        page_size: Number of items per page

    Returns:
        Tuple of (items, total_count, page, page_size, total_pages)
    """
    if page_size is None:
        page_size = settings.DEFAULT_PAGE_SIZE

    # Ensure page_size is within limits
    page_size = min(page_size, settings.MAX_PAGE_SIZE)
    page_size = max(page_size, 1)

    # Ensure page is at least 1
    page = max(page, 1)

    # Get total count
    total = query.count()

    # Calculate total pages
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    # Ensure page doesn't exceed total_pages
    page = min(page, total_pages)

    # Get paginated items
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return items, total, page, page_size, total_pages


def create_paginated_response(
    items: List[T],
    total: int,
    page: int,
    page_size: int,
    total_pages: int
) -> PaginatedResponse[T]:
    """
    Create a paginated response.

    Args:
        items: List of items
        total: Total count
        page: Current page
        page_size: Page size
        total_pages: Total pages

    Returns:
        PaginatedResponse object
    """
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
