"""Influencer payout model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class PayoutStatus(str, enum.Enum):
    """Payout status."""
    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
    CANCELLED = "cancelled"


class PaymentMethod(str, enum.Enum):
    """Payment method."""
    ACH = "ach"
    CHECK = "check"
    PAYPAL = "paypal"
    WIRE = "wire"
    VENMO = "venmo"


class InfluencerPayout(Base):
    """Influencer payout model - tracks payments to influencers."""

    __tablename__ = "influencer_payouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    influencer_id = Column(Integer, ForeignKey("influencers.id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    total_sales = Column(Numeric(10, 2), nullable=False, default=0.00)  # From promo codes
    commission_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    flat_fee = Column(Numeric(10, 2), nullable=False, default=0.00)  # For contracted posts
    total_payout = Column(Numeric(10, 2), nullable=False, default=0.00)
    status = Column(
        SQLEnum(PayoutStatus, name="payout_status", create_type=True),
        nullable=False,
        default=PayoutStatus.PENDING
    )
    paid_at = Column(DateTime(timezone=True), nullable=True)
    payment_method = Column(
        SQLEnum(PaymentMethod, name="payment_method", create_type=True),
        nullable=True
    )
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    influencer = relationship("Influencer", back_populates="payouts")

    def __repr__(self):
        return f"<InfluencerPayout influencer_id={self.influencer_id} ${self.total_payout}>"
