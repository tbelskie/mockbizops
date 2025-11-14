"""Campaign schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.domains.marketing.models import CampaignObjective, CampaignStatus


class CampaignResponse(BaseModel):
    """Campaign response schema."""
    id: int
    campaign_id: str
    ad_account_id: int
    name: str
    objective: CampaignObjective
    status: CampaignStatus
    daily_budget: Optional[Decimal]
    lifetime_budget: Optional[Decimal]
    start_time: Optional[datetime]
    stop_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignListResponse(BaseModel):
    """Campaign list response schema."""
    id: int
    campaign_id: str
    name: str
    objective: CampaignObjective
    status: CampaignStatus
    daily_budget: Optional[Decimal]
    lifetime_budget: Optional[Decimal]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
