"""Promo code model."""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class DiscountType(str, enum.Enum):
    """Discount type."""
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


class PromoCodeStatus(str, enum.Enum):
    """Promo code status."""
    ACTIVE = "active"
    EXPIRED = "expired"
    DISABLED = "disabled"


class PromoCode(Base):
    """Promo code model - represents promotional discount codes."""

    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    influencer_id = Column(Integer, ForeignKey("influencers.id"), nullable=False)
    discount_type = Column(
        SQLEnum(DiscountType, name="discount_type", create_type=True),
        nullable=False,
        default=DiscountType.PERCENTAGE
    )
    discount_value = Column(Numeric(10, 2), nullable=False)  # e.g., 10.00 for 10% or $10
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    usage_limit = Column(Integer, nullable=True)  # NULL for unlimited
    usage_count = Column(Integer, nullable=False, default=0)
    status = Column(
        SQLEnum(PromoCodeStatus, name="promo_code_status", create_type=True),
        nullable=False,
        default=PromoCodeStatus.ACTIVE
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    influencer = relationship("Influencer", back_populates="promo_codes")
    usage_records = relationship("PromoCodeUsage", back_populates="promo_code", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PromoCode {self.code} - {self.influencer_id}>"
