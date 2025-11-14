"""Promo code schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

from app.domains.marketing.models import DiscountType, PromoCodeStatus


class PromoCodeResponse(BaseModel):
    """Promo code response schema."""
    id: int
    code: str
    influencer_id: int
    discount_type: DiscountType
    discount_value: Decimal
    start_date: date
    end_date: Optional[date]
    usage_limit: Optional[int]
    usage_count: int
    status: PromoCodeStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PromoCodeListResponse(BaseModel):
    """Promo code list response schema."""
    id: int
    code: str
    influencer_id: int
    discount_type: DiscountType
    discount_value: Decimal
    usage_count: int
    status: PromoCodeStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PromoCodeUsageResponse(BaseModel):
    """Promo code usage response schema."""
    id: int
    promo_code_id: int
    used_at: datetime
    order_id: str
    order_value: Decimal
    discount_amount: Decimal
    customer_id: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
