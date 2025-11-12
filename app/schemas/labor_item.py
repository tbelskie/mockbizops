"""Labor item schemas."""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class LaborItemBase(BaseModel):
    """Base labor item schema."""
    description: str = Field(..., min_length=1, max_length=255)
    hours: Decimal = Field(..., ge=0, decimal_places=2)
    hourly_rate: Decimal = Field(..., ge=0, decimal_places=2)


class LaborItemResponse(LaborItemBase):
    """Labor item response schema."""
    id: UUID
    work_order_id: UUID
    mechanic_id: UUID
    total_cost: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LaborItemWithMechanic(LaborItemResponse):
    """Labor item response with mechanic details."""
    mechanic_first_name: str
    mechanic_last_name: str
    mechanic_certification: str

    model_config = ConfigDict(from_attributes=True)
