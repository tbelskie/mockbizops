"""Ad insight schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class AdInsightListResponse(BaseModel):
    """Ad insight list response schema."""
    id: int
    ad_id: int
    date_start: date
    date_stop: date
    impressions: int
    clicks: int
    spend: Decimal
    reach: int
    cpc: Optional[Decimal]
    cpm: Optional[Decimal]
    ctr: Optional[Decimal]
    conversions: int

    model_config = ConfigDict(from_attributes=True)


class AdInsightResponse(BaseModel):
    """Ad insight response schema."""
    id: int
    ad_id: int
    date_start: date
    date_stop: date
    impressions: int
    clicks: int
    spend: Decimal
    reach: int
    frequency: Optional[Decimal]
    cpc: Optional[Decimal]
    cpm: Optional[Decimal]
    ctr: Optional[Decimal]
    conversions: int
    conversion_value: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
