"""Part model."""
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Part(Base):
    """Part model."""

    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    part_number = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    total_cost = Column(Numeric(10, 2), nullable=False)  # quantity * unit_cost
    supplier = Column(String(100), nullable=False)
    warranty_months = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    work_order = relationship("WorkOrder", back_populates="parts")

    def __repr__(self):
        return f"<Part {self.part_number} - {self.description}>"
