"""Work Order Service Job association model."""
from sqlalchemy import Column, Integer, ForeignKey, Numeric, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class WorkOrderServiceJob(Base):
    """Association table linking work orders to service jobs with actual hours."""

    __tablename__ = "work_order_service_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    service_job_id = Column(Integer, ForeignKey("service_jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    hours_actual = Column(Numeric(5, 2), nullable=False)  # Actual hours for this job on this work order
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    work_order = relationship("WorkOrder", back_populates="service_job_associations")
    service_job = relationship("ServiceJob", back_populates="work_order_associations")

    def __repr__(self):
        return f"<WorkOrderServiceJob WO:{self.work_order_id} Job:{self.service_job_id}>"
