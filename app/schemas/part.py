"""Part schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class PartBase(BaseModel):
    """Base part schema."""
    part_number: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=255)
    quantity: int = Field(..., ge=1)
    unit_cost: Decimal = Field(..., ge=0, decimal_places=2)
    supplier: str = Field(..., min_length=1, max_length=100)
    warranty_months: Optional[int] = Field(None, ge=0)


class PartResponse(PartBase):
    """Part response schema."""
    id: UUID
    work_order_id: UUID
    total_cost: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PartListResponse(BaseModel):
    """Simplified part response for list views."""
    id: UUID
    part_number: str
    description: str
    quantity: int
    unit_cost: Decimal
    total_cost: Decimal

    model_config = ConfigDict(from_attributes=True)
