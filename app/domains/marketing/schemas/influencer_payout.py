"""Influencer payout schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

from app.domains.marketing.models import PayoutStatus, PaymentMethod


class InfluencerPayoutResponse(BaseModel):
    """Influencer payout response schema."""
    id: int
    influencer_id: int
    period_start: date
    period_end: date
    total_sales: Decimal
    commission_amount: Decimal
    flat_fee: Decimal
    total_payout: Decimal
    status: PayoutStatus
    paid_at: Optional[datetime]
    payment_method: Optional[PaymentMethod]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InfluencerPayoutListResponse(BaseModel):
    """Influencer payout list response schema."""
    id: int
    influencer_id: int
    period_start: date
    period_end: date
    total_payout: Decimal
    status: PayoutStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
