"""API Key schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class APIKeyCreate(BaseModel):
    """API key creation schema."""
    name: str = Field(..., min_length=1, max_length=255, description="Description or name for this API key")


class APIKeyResponse(BaseModel):
    """API key response schema."""
    id: UUID
    key: str
    name: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class APIKeyListResponse(BaseModel):
    """Simplified API key response for list views."""
    id: UUID
    name: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]
    # Note: We don't include the actual key in list responses for security

    model_config = ConfigDict(from_attributes=True)
