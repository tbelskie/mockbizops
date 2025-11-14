"""Ad insights API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import get_marketing_db
from app.auth import get_api_key
from app.domains.marketing.models import AdInsight
from app.domains.marketing.schemas import (
    AdInsightListResponse,
    AdInsightResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/ad-insights", tags=["marketing-ad-insights"])


@router.get("", response_model=PaginatedResponse[AdInsightListResponse])
async def list_ad_insights(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    ad_id: Optional[int] = Query(None, description="Filter by ad ID"),
    date_start: Optional[date] = Query(None, description="Filter by start date"),
    date_stop: Optional[date] = Query(None, description="Filter by end date"),
    db: Session = Depends(get_marketing_db),
    api_key: str = Depends(get_api_key)
):
    """List all ad insights with pagination and filtering."""
    query = db.query(AdInsight)

    # Apply filters
    if ad_id:
        query = query.filter(AdInsight.ad_id == ad_id)
    if date_start:
        query = query.filter(AdInsight.date_start >= date_start)
    if date_stop:
        query = query.filter(AdInsight.date_stop <= date_stop)

    # Apply sorting
    query = query.order_by(AdInsight.date_start.desc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{insight_id}", response_model=AdInsightResponse)
async def get_ad_insight(
    insight_id: int,
    db: Session = Depends(get_marketing_db),
    api_key: str = Depends(get_api_key)
):
    """Get detailed ad insight information."""
    insight = db.query(AdInsight).filter(AdInsight.id == insight_id).first()

    if not insight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ad insight with ID {insight_id} not found"
        )

    return insight
