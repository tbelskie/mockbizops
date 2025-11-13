"""Mechanic schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime

from decimal import Decimal
from app.models.mechanic import CertificationLevel


class MechanicBase(BaseModel):
    """Base mechanic schema."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    certification_level: CertificationLevel
    specialties: List[str] = Field(..., min_items=1)
    hourly_rate: Decimal = Field(..., ge=0, decimal_places=2)
    is_active: bool = True


class MechanicResponse(MechanicBase):
    """Mechanic response schema."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MechanicListResponse(BaseModel):
    """Simplified mechanic response for list views."""
    id: int
    first_name: str
    last_name: str
    certification_level: CertificationLevel
    specialties: List[str]
    hourly_rate: Decimal
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
