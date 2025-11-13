"""Parts API endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional


from app.database import get_db
from app.auth import get_api_key
from app.models import Part
from app.schemas import PartResponse, PaginatedResponse
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/parts", tags=["parts"])


@router.get("", response_model=PaginatedResponse[PartResponse])
async def list_parts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    work_order_id: Optional[int] = Query(None, description="Filter by work order ID"),
    part_number: Optional[str] = Query(None, description="Filter by part number"),
    supplier: Optional[str] = Query(None, description="Filter by supplier"),
    sort_by: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all parts with pagination and filtering."""
    query = db.query(Part)

    # Apply filters
    if work_order_id:
        query = query.filter(Part.work_order_id == work_order_id)
    if part_number:
        query = query.filter(Part.part_number.ilike(f"%{part_number}%"))
    if supplier:
        query = query.filter(Part.supplier.ilike(f"%{supplier}%"))

    # Apply sorting
    sort_column = getattr(Part, sort_by, Part.created_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Paginate
    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)
