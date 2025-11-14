"""Influencer content model."""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class ContentPlatform(str, enum.Enum):
    """Content platform."""
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    TWITTER = "twitter"


class ContentType(str, enum.Enum):
    """Content type."""
    STORY = "story"
    REEL = "reel"
    POST = "post"
    VIDEO = "video"
    LIVE = "live"


class InfluencerContent(Base):
    """Influencer content model - tracks posts/content created by influencers."""

    __tablename__ = "influencer_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    influencer_id = Column(Integer, ForeignKey("influencers.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)  # Optional
    ad_id = Column(Integer, ForeignKey("ads.id"), nullable=True)  # Optional if it's a paid ad
    platform = Column(
        SQLEnum(ContentPlatform, name="content_platform", create_type=True),
        nullable=False,
        default=ContentPlatform.INSTAGRAM
    )
    post_url = Column(String(500), nullable=False)
    post_type = Column(
        SQLEnum(ContentType, name="content_type", create_type=True),
        nullable=False,
        default=ContentType.POST
    )
    post_date = Column(DateTime(timezone=True), nullable=False)
    impressions = Column(Integer, nullable=False, default=0)
    likes = Column(Integer, nullable=False, default=0)
    comments = Column(Integer, nullable=False, default=0)
    shares = Column(Integer, nullable=False, default=0)
    saves = Column(Integer, nullable=False, default=0)
    engagement_rate = Column(Numeric(5, 2), nullable=True)  # Percentage
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    influencer = relationship("Influencer", back_populates="content")
    campaign = relationship("Campaign")
    ad = relationship("Ad")

    def __repr__(self):
        return f"<InfluencerContent influencer_id={self.influencer_id} {self.platform} {self.post_type}>"
