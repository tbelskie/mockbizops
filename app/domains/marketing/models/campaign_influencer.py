"""Campaign influencer model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class InfluencerRole(str, enum.Enum):
    """Influencer role in campaign."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    AMBASSADOR = "ambassador"


class CampaignInfluencer(Base):
    """Campaign influencer model - links campaigns to influencers."""

    __tablename__ = "campaign_influencers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    influencer_id = Column(Integer, ForeignKey("influencers.id"), nullable=False)
    role = Column(
        SQLEnum(InfluencerRole, name="influencer_role", create_type=True),
        nullable=False,
        default=InfluencerRole.SECONDARY
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    campaign = relationship("Campaign", back_populates="campaign_influencers")
    influencer = relationship("Influencer", back_populates="campaign_associations")

    def __repr__(self):
        return f"<CampaignInfluencer campaign_id={self.campaign_id} influencer_id={self.influencer_id}>"
