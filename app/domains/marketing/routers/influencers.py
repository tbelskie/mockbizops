"""Influencer API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_marketing_db
from app.auth import get_api_key
from app.domains.marketing.models import Influencer, InfluencerStatus
from app.domains.marketing.schemas import (
    InfluencerListResponse,
    InfluencerResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/influencers", tags=["marketing-influencers"])


@router.get("", response_model=PaginatedResponse[InfluencerListResponse])
async def list_influencers(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[InfluencerStatus] = Query(None, description="Filter by status"),
    db: Session = Depends(get_marketing_db),
    api_key: str = Depends(get_api_key)
):
    """List all influencers with pagination and filtering."""
    query = db.query(Influencer)

    # Apply filters
    if status:
        query = query.filter(Influencer.status == status)

    # Apply sorting
    query = query.order_by(Influencer.created_at.desc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{influencer_id}", response_model=InfluencerResponse)
async def get_influencer(
    influencer_id: int,
    db: Session = Depends(get_marketing_db),
    api_key: str = Depends(get_api_key)
):
    """Get detailed influencer information."""
    influencer = db.query(Influencer).filter(Influencer.id == influencer_id).first()

    if not influencer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Influencer with ID {influencer_id} not found"
        )

    return influencer
