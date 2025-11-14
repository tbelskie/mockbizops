"""Service job schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.domains.auto_shop.models.service_job import ServiceJobCategory


class ServiceJobBase(BaseModel):
    """Base service job schema."""
    job_code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: ServiceJobCategory
    standard_hours: Decimal = Field(..., ge=0, decimal_places=2)


class ServiceJobResponse(ServiceJobBase):
    """Service job response schema."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceJobListResponse(BaseModel):
    """Simplified service job response for list views."""
    id: int
    job_code: str
    name: str
    category: ServiceJobCategory
    standard_hours: Decimal

    model_config = ConfigDict(from_attributes=True)
