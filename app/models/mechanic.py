"""Mechanic model."""
import uuid
from sqlalchemy import Column, String, Boolean, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class CertificationLevel(str, enum.Enum):
    """Mechanic certification levels."""
    APPRENTICE = "Apprentice"
    JOURNEYMAN = "Journeyman"
    MASTER = "Master"


class Mechanic(Base):
    """Mechanic model."""

    __tablename__ = "mechanics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    certification_level = Column(
        SQLEnum(CertificationLevel, name="certification_level", create_type=True),
        nullable=False,
        default=CertificationLevel.JOURNEYMAN
    )
    specialties = Column(JSONB, nullable=False, default=list)  # Array of specialties
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    work_orders = relationship("WorkOrder", back_populates="assigned_mechanic")
    labor_items = relationship("LaborItem", back_populates="mechanic")

    def __repr__(self):
        return f"<Mechanic {self.first_name} {self.last_name} ({self.certification_level})>"
