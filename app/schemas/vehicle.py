"""Vehicle schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class VehicleBase(BaseModel):
    """Base vehicle schema."""
    vin: str = Field(..., min_length=17, max_length=17)
    year: int = Field(..., ge=1900, le=2030)
    make: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    trim: Optional[str] = Field(None, max_length=50)
    color: str = Field(..., min_length=1, max_length=30)
    license_plate: str = Field(..., min_length=1, max_length=20)
    mileage: int = Field(..., ge=0)


class VehicleResponse(VehicleBase):
    """Vehicle response schema."""
    id: UUID
    customer_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VehicleListResponse(BaseModel):
    """Simplified vehicle response for list views."""
    id: UUID
    customer_id: UUID
    year: int
    make: str
    model: str
    color: str
    license_plate: str
    mileage: int

    model_config = ConfigDict(from_attributes=True)


class VehicleWithCustomer(VehicleResponse):
    """Vehicle response with customer details."""
    customer_first_name: str
    customer_last_name: str
    customer_email: str
    customer_phone: str

    model_config = ConfigDict(from_attributes=True)
