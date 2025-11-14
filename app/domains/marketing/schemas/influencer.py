"""Influencer schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

from app.domains.marketing.models import InfluencerStatus, PaymentTerms


class InfluencerBase(BaseModel):
    """Base influencer schema."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    instagram_handle: Optional[str] = Field(None, max_length=100)
    tiktok_handle: Optional[str] = Field(None, max_length=100)
    youtube_channel: Optional[str] = Field(None, max_length=255)
    follower_count: int = Field(0, ge=0)
    engagement_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    commission_rate: Decimal = Field(0.10, ge=0, le=1)
    flat_rate_per_post: Optional[Decimal] = Field(None, ge=0)
    payment_terms: PaymentTerms = PaymentTerms.NET_30
    status: InfluencerStatus = InfluencerStatus.ACTIVE


class InfluencerResponse(InfluencerBase):
    """Influencer response schema."""
    id: int
    contract_start_date: Optional[date]
    contract_end_date: Optional[date]
    tax_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InfluencerListResponse(BaseModel):
    """Influencer list response schema."""
    id: int
    first_name: str
    last_name: str
    email: str
    instagram_handle: Optional[str]
    tiktok_handle: Optional[str]
    follower_count: int
    engagement_rate: Optional[Decimal]
    commission_rate: Decimal
    status: InfluencerStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
