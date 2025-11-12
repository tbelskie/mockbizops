"""Customer schemas."""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime, date
from uuid import UUID


class CustomerBase(BaseModel):
    """Base customer schema."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., min_length=5, max_length=10)
    notes: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Customer response schema."""
    id: UUID
    customer_since: date
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerListResponse(BaseModel):
    """Simplified customer response for list views."""
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    city: str
    state: str
    customer_since: date

    model_config = ConfigDict(from_attributes=True)
