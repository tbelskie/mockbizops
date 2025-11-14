"""Campaign API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_marketing_db
from app.auth import get_api_key
from app.domains.marketing.models import Campaign, CampaignStatus, CampaignObjective
from app.domains.marketing.schemas import (
    CampaignListResponse,
    CampaignResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/campaigns", tags=["marketing-campaigns"])


@router.get("", response_model=PaginatedResponse[CampaignListResponse])
async def list_campaigns(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[CampaignStatus] = Query(None, description="Filter by status"),
    objective: Optional[CampaignObjective] = Query(None, description="Filter by objective"),
    db: Session = Depends(get_marketing_db),
    api_key: str = Depends(get_api_key)
):
    """List all campaigns with pagination and filtering."""
    query = db.query(Campaign)

    # Apply filters
    if status:
        query = query.filter(Campaign.status == status)
    if objective:
        query = query.filter(Campaign.objective == objective)

    # Apply sorting
    query = query.order_by(Campaign.created_at.desc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_marketing_db),
    api_key: str = Depends(get_api_key)
):
    """Get detailed campaign information."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID {campaign_id} not found"
        )

    return campaign
