"""Promo code API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.auth import get_api_key
from app.domains.marketing.models import PromoCode, PromoCodeUsage, PromoCodeStatus
from app.domains.marketing.schemas import (
    PromoCodeListResponse,
    PromoCodeResponse,
    PromoCodeUsageResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/promo-codes", tags=["marketing-promo-codes"])


@router.get("", response_model=PaginatedResponse[PromoCodeListResponse])
async def list_promo_codes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[PromoCodeStatus] = Query(None, description="Filter by status"),
    influencer_id: Optional[int] = Query(None, description="Filter by influencer ID"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all promo codes with pagination and filtering."""
    query = db.query(PromoCode)

    # Apply filters
    if status:
        query = query.filter(PromoCode.status == status)
    if influencer_id:
        query = query.filter(PromoCode.influencer_id == influencer_id)

    # Apply sorting
    query = query.order_by(PromoCode.created_at.desc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{promo_code_id}", response_model=PromoCodeResponse)
async def get_promo_code(
    promo_code_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get detailed promo code information."""
    promo_code = db.query(PromoCode).filter(PromoCode.id == promo_code_id).first()

    if not promo_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Promo code with ID {promo_code_id} not found"
        )

    return promo_code


@router.get("/{promo_code_id}/usage", response_model=PaginatedResponse[PromoCodeUsageResponse])
async def get_promo_code_usage(
    promo_code_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get usage history for a specific promo code."""
    # Check if promo code exists
    promo_code = db.query(PromoCode).filter(PromoCode.id == promo_code_id).first()
    if not promo_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Promo code with ID {promo_code_id} not found"
        )

    query = db.query(PromoCodeUsage).filter(PromoCodeUsage.promo_code_id == promo_code_id)
    query = query.order_by(PromoCodeUsage.used_at.desc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)
