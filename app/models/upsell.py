"""Upsell model for tracking additional services recommended."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class UpsellStatus(str, enum.Enum):
    """Upsell status."""
    PROPOSED = "proposed"
    APPROVED = "approved"
    DECLINED = "declined"
    COMPLETED = "completed"


class Upsell(Base):
    """Upsell model - tracks additional services recommended beyond original work order."""

    __tablename__ = "upsells"

    id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    recommended_by_mechanic_id = Column(Integer, ForeignKey("mechanics.id"), nullable=False, index=True)

    description = Column(Text, nullable=False)  # What additional work is recommended
    reason = Column(Text, nullable=True)  # Why this work is needed

    # Financial tracking
    estimated_amount = Column(Numeric(10, 2), nullable=False)  # Initial estimate
    actual_amount = Column(Numeric(10, 2), nullable=True)  # Final amount if completed

    # Commission tracking
    commission_rate = Column(Numeric(5, 4), nullable=False, default=0.10)  # Default 10%
    commission_amount = Column(Numeric(10, 2), nullable=True)  # Calculated commission

    # Status tracking
    status = Column(
        SQLEnum(UpsellStatus, name="upsell_status", create_type=True),
        nullable=False,
        default=UpsellStatus.PROPOSED,
        index=True
    )

    # Approval tracking
    proposed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Notes
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    work_order = relationship("WorkOrder", back_populates="upsells")
    recommended_by = relationship("Mechanic", back_populates="upsells_recommended")

    def __repr__(self):
        return f"<Upsell {self.id} - WO:{self.work_order_id} - {self.status}>"

    def calculate_commission(self):
        """Calculate commission based on actual or estimated amount."""
        amount = self.actual_amount if self.actual_amount else self.estimated_amount
        if amount and self.status in [UpsellStatus.APPROVED, UpsellStatus.COMPLETED]:
            self.commission_amount = amount * self.commission_rate
        else:
            self.commission_amount = None
        return self.commission_amount
