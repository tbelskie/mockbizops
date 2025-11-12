"""Work order model."""
import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class WorkOrderStatus(str, enum.Enum):
    """Work order status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING_PARTS = "waiting_parts"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class WorkOrderPriority(str, enum.Enum):
    """Work order priority."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class PaymentStatus(str, enum.Enum):
    """Payment status."""
    UNPAID = "unpaid"
    PARTIAL = "partial"
    PAID = "paid"


class PaymentMethod(str, enum.Enum):
    """Payment method."""
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CHECK = "check"


class WorkOrder(Base):
    """Work order model."""

    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_order_number = Column(String(50), nullable=False, unique=True, index=True)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_mechanic_id = Column(UUID(as_uuid=True), ForeignKey("mechanics.id"), nullable=True, index=True)

    status = Column(
        SQLEnum(WorkOrderStatus, name="work_order_status", create_type=True),
        nullable=False,
        default=WorkOrderStatus.PENDING,
        index=True
    )
    priority = Column(
        SQLEnum(WorkOrderPriority, name="work_order_priority", create_type=True),
        nullable=False,
        default=WorkOrderPriority.NORMAL,
        index=True
    )

    description = Column(Text, nullable=False)
    customer_concern = Column(Text, nullable=False)
    diagnosis = Column(Text, nullable=True)

    estimated_completion = Column(DateTime(timezone=True), nullable=True)
    actual_completion = Column(DateTime(timezone=True), nullable=True)

    odometer_in = Column(Integer, nullable=False)
    odometer_out = Column(Integer, nullable=True)

    # Financial fields
    subtotal_parts = Column(Numeric(10, 2), nullable=False, default=0.00)
    subtotal_labor = Column(Numeric(10, 2), nullable=False, default=0.00)
    tax_rate = Column(Numeric(5, 4), nullable=False, default=0.08)
    tax_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)

    payment_status = Column(
        SQLEnum(PaymentStatus, name="payment_status", create_type=True),
        nullable=False,
        default=PaymentStatus.UNPAID,
        index=True
    )
    payment_method = Column(
        SQLEnum(PaymentMethod, name="payment_method", create_type=True),
        nullable=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    vehicle = relationship("Vehicle", back_populates="work_orders")
    customer = relationship("Customer", back_populates="work_orders")
    assigned_mechanic = relationship("Mechanic", back_populates="work_orders")
    parts = relationship("Part", back_populates="work_order", cascade="all, delete-orphan")
    labor_items = relationship("LaborItem", back_populates="work_order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WorkOrder {self.work_order_number}>"
