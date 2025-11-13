"""Upsell schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.upsell import UpsellStatus


class UpsellBase(BaseModel):
    """Base upsell schema."""
    description: str = Field(..., min_length=1)
    reason: Optional[str] = None
    estimated_amount: Decimal = Field(..., ge=0, decimal_places=2)
    commission_rate: Decimal = Field(default=Decimal("0.10"), ge=0, le=1, decimal_places=4)


class UpsellCreate(UpsellBase):
    """Create upsell schema."""
    work_order_id: int
    recommended_by_mechanic_id: int


class UpsellResponse(UpsellBase):
    """Upsell response schema."""
    id: int
    work_order_id: int
    recommended_by_mechanic_id: int
    actual_amount: Optional[Decimal]
    commission_amount: Optional[Decimal]
    status: UpsellStatus
    proposed_at: datetime
    approved_at: Optional[datetime]
    completed_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpsellListResponse(BaseModel):
    """Simplified upsell response for list views."""
    id: int
    work_order_id: int
    work_order_number: str
    recommended_by_first_name: str
    recommended_by_last_name: str
    description: str
    estimated_amount: Decimal
    actual_amount: Optional[Decimal]
    commission_amount: Optional[Decimal]
    status: UpsellStatus
    proposed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpsellUpdateStatus(BaseModel):
    """Update upsell status."""
    status: UpsellStatus
    actual_amount: Optional[Decimal] = None
    notes: Optional[str] = None


class MechanicCommissionSummary(BaseModel):
    """Summary of mechanic's upsell commissions."""
    mechanic_id: int
    mechanic_first_name: str
    mechanic_last_name: str
    total_upsells_proposed: int
    total_upsells_approved: int
    total_upsells_completed: int
    approval_rate: Decimal  # percentage
    total_commission_earned: Decimal
    pending_commission: Decimal  # approved but not completed

    model_config = ConfigDict(from_attributes=True)
