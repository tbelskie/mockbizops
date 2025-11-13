"""Service job model."""
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class ServiceJobCategory(str, enum.Enum):
    """Service job categories."""
    MAINTENANCE = "Maintenance"
    REPAIR = "Repair"
    INSPECTION = "Inspection"
    DIAGNOSTIC = "Diagnostic"


class ServiceJob(Base):
    """Service job model - predefined service types with job codes."""

    __tablename__ = "service_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_code = Column(String(50), nullable=False, unique=True, index=True)  # e.g., "OIL-CHANGE"
    name = Column(String(255), nullable=False)  # e.g., "Oil Change"
    description = Column(Text, nullable=True)
    category = Column(
        SQLEnum(ServiceJobCategory, name="service_job_category", create_type=True),
        nullable=False,
        default=ServiceJobCategory.MAINTENANCE
    )
    standard_hours = Column(Numeric(5, 2), nullable=False)  # Typical time to complete
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    work_order_associations = relationship("WorkOrderServiceJob", back_populates="service_job")

    def __repr__(self):
        return f"<ServiceJob {self.job_code} - {self.name}>"
