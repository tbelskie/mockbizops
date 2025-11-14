"""Campaign model."""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class CampaignObjective(str, enum.Enum):
    """Campaign objectives."""
    BRAND_AWARENESS = "brand_awareness"
    REACH = "reach"
    TRAFFIC = "traffic"
    ENGAGEMENT = "engagement"
    APP_INSTALLS = "app_installs"
    VIDEO_VIEWS = "video_views"
    LEAD_GENERATION = "lead_generation"
    MESSAGES = "messages"
    CONVERSIONS = "conversions"
    CATALOG_SALES = "catalog_sales"
    STORE_TRAFFIC = "store_traffic"


class CampaignStatus(str, enum.Enum):
    """Campaign status."""
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"
    ARCHIVED = "archived"


class Campaign(Base):
    """Campaign model - represents a Meta Ads campaign."""

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(String(50), nullable=False, unique=True, index=True)  # Meta campaign ID
    ad_account_id = Column(Integer, ForeignKey("ad_accounts.id"), nullable=False)
    name = Column(String(255), nullable=False)
    objective = Column(
        SQLEnum(CampaignObjective, name="campaign_objective", create_type=True),
        nullable=False,
        default=CampaignObjective.CONVERSIONS
    )
    status = Column(
        SQLEnum(CampaignStatus, name="campaign_status", create_type=True),
        nullable=False,
        default=CampaignStatus.ACTIVE
    )
    daily_budget = Column(Numeric(10, 2), nullable=True)
    lifetime_budget = Column(Numeric(10, 2), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=True)
    stop_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    ad_account = relationship("AdAccount", back_populates="campaigns")
    ad_sets = relationship("AdSet", back_populates="campaign", cascade="all, delete-orphan")
    campaign_influencers = relationship("CampaignInfluencer", back_populates="campaign", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campaign {self.campaign_id} - {self.name}>"
