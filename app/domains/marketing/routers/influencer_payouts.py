"""Influencer payout API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.auth import get_api_key
from app.domains.marketing.models import InfluencerPayout, PayoutStatus
from app.domains.marketing.schemas import (
    InfluencerPayoutListResponse,
    InfluencerPayoutResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/influencer-payouts", tags=["marketing-influencer-payouts"])


@router.get("", response_model=PaginatedResponse[InfluencerPayoutListResponse])
async def list_influencer_payouts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[PayoutStatus] = Query(None, description="Filter by status"),
    influencer_id: Optional[int] = Query(None, description="Filter by influencer ID"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all influencer payouts with pagination and filtering."""
    query = db.query(InfluencerPayout)

    # Apply filters
    if status:
        query = query.filter(InfluencerPayout.status == status)
    if influencer_id:
        query = query.filter(InfluencerPayout.influencer_id == influencer_id)

    # Apply sorting
    query = query.order_by(InfluencerPayout.created_at.desc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{payout_id}", response_model=InfluencerPayoutResponse)
async def get_influencer_payout(
    payout_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get detailed influencer payout information."""
    payout = db.query(InfluencerPayout).filter(InfluencerPayout.id == payout_id).first()

    if not payout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Influencer payout with ID {payout_id} not found"
        )

    return payout
