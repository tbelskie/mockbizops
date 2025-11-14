"""Influencer model."""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Numeric, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class InfluencerStatus(str, enum.Enum):
    """Influencer status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class PaymentTerms(str, enum.Enum):
    """Payment terms."""
    NET_15 = "net_15"
    NET_30 = "net_30"
    NET_45 = "net_45"
    NET_60 = "net_60"
    IMMEDIATE = "immediate"


class Influencer(Base):
    """Influencer model - represents influencers/contractors."""

    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    instagram_handle = Column(String(100), nullable=True)
    tiktok_handle = Column(String(100), nullable=True)
    youtube_channel = Column(String(255), nullable=True)
    follower_count = Column(Integer, nullable=False, default=0)
    engagement_rate = Column(Numeric(5, 2), nullable=True)  # Percentage
    contract_start_date = Column(Date, nullable=True)
    contract_end_date = Column(Date, nullable=True)
    commission_rate = Column(Numeric(5, 4), nullable=False, default=0.10)  # e.g., 0.10 for 10%
    flat_rate_per_post = Column(Numeric(10, 2), nullable=True)
    payment_terms = Column(
        SQLEnum(PaymentTerms, name="payment_terms", create_type=True),
        nullable=False,
        default=PaymentTerms.NET_30
    )
    tax_id = Column(String(20), nullable=True)  # For 1099 contractors
    status = Column(
        SQLEnum(InfluencerStatus, name="influencer_status", create_type=True),
        nullable=False,
        default=InfluencerStatus.ACTIVE
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    promo_codes = relationship("PromoCode", back_populates="influencer", cascade="all, delete-orphan")
    payouts = relationship("InfluencerPayout", back_populates="influencer", cascade="all, delete-orphan")
    content = relationship("InfluencerContent", back_populates="influencer", cascade="all, delete-orphan")
    campaign_associations = relationship("CampaignInfluencer", back_populates="influencer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Influencer {self.first_name} {self.last_name} - @{self.instagram_handle}>"
