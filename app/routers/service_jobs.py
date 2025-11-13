"""Service Jobs API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.auth import get_api_key
from app.models import ServiceJob, ServiceJobCategory
from app.schemas import (
    ServiceJobResponse,
    ServiceJobListResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/service-jobs", tags=["service-jobs"])


@router.get("", response_model=PaginatedResponse[ServiceJobListResponse])
async def list_service_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    category: Optional[ServiceJobCategory] = Query(None, description="Filter by category"),
    sort_by: str = Query("job_code", description="Sort field"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all available service jobs with pagination and filtering."""
    query = db.query(ServiceJob)

    # Apply category filter
    if category:
        query = query.filter(ServiceJob.category == category)

    # Apply sorting
    sort_column = getattr(ServiceJob, sort_by, ServiceJob.job_code)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Paginate
    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{service_job_id}", response_model=ServiceJobResponse)
async def get_service_job(
    service_job_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific service job by ID."""
    service_job = db.query(ServiceJob).filter(ServiceJob.id == service_job_id).first()

    if not service_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service job with ID {service_job_id} not found"
        )

    return service_job
