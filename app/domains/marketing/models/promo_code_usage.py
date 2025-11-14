"""Promo code usage model."""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class PromoCodeUsage(Base):
    """Promo code usage model - tracks when promo codes are used."""

    __tablename__ = "promo_code_usage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    promo_code_id = Column(Integer, ForeignKey("promo_codes.id"), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    order_id = Column(String(100), nullable=False)  # Reference to e-commerce order
    order_value = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), nullable=False)
    customer_id = Column(String(100), nullable=True)  # Optional customer reference
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    promo_code = relationship("PromoCode", back_populates="usage_records")

    def __repr__(self):
        return f"<PromoCodeUsage promo_code_id={self.promo_code_id} order_id={self.order_id}>"
