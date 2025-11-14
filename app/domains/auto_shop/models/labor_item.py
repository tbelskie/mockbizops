"""Labor item model."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class LaborItem(Base):
    """Labor item model."""

    __tablename__ = "labor_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    hours = Column(Numeric(5, 2), nullable=False)
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    total_cost = Column(Numeric(10, 2), nullable=False)  # hours * hourly_rate
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    work_order = relationship("WorkOrder", back_populates="labor_items")
    mechanic = relationship("Mechanic", back_populates="labor_items")

    def __repr__(self):
        return f"<LaborItem {self.description}>"
