"""Ad set model."""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Numeric, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class OptimizationGoal(str, enum.Enum):
    """Optimization goals."""
    IMPRESSIONS = "impressions"
    LINK_CLICKS = "link_clicks"
    REACH = "reach"
    LANDING_PAGE_VIEWS = "landing_page_views"
    POST_ENGAGEMENT = "post_engagement"
    CONVERSIONS = "conversions"
    VALUE = "value"
    THRUPLAY = "thruplay"


class BillingEvent(str, enum.Enum):
    """Billing events."""
    IMPRESSIONS = "impressions"
    LINK_CLICKS = "link_clicks"
    POST_ENGAGEMENT = "post_engagement"
    THRUPLAY = "thruplay"


class AdSetStatus(str, enum.Enum):
    """Ad set status."""
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"
    ARCHIVED = "archived"


class AdSet(Base):
    """Ad set model - represents a Meta Ads ad set."""

    __tablename__ = "ad_sets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_set_id = Column(String(50), nullable=False, unique=True, index=True)  # Meta ad set ID
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    name = Column(String(255), nullable=False)
    optimization_goal = Column(
        SQLEnum(OptimizationGoal, name="optimization_goal", create_type=True),
        nullable=False,
        default=OptimizationGoal.CONVERSIONS
    )
    billing_event = Column(
        SQLEnum(BillingEvent, name="billing_event", create_type=True),
        nullable=False,
        default=BillingEvent.IMPRESSIONS
    )
    bid_amount = Column(Numeric(10, 2), nullable=True)
    daily_budget = Column(Numeric(10, 2), nullable=True)
    lifetime_budget = Column(Numeric(10, 2), nullable=True)
    targeting = Column(JSON, nullable=True)  # JSON with age, gender, interests, locations
    status = Column(
        SQLEnum(AdSetStatus, name="ad_set_status", create_type=True),
        nullable=False,
        default=AdSetStatus.ACTIVE
    )
    start_time = Column(DateTime(timezone=True), nullable=True)
    stop_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    campaign = relationship("Campaign", back_populates="ad_sets")
    ads = relationship("Ad", back_populates="ad_set", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AdSet {self.ad_set_id} - {self.name}>"
