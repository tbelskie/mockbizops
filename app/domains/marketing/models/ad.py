"""Ad model."""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class AdStatus(str, enum.Enum):
    """Ad status."""
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"
    ARCHIVED = "archived"


class Ad(Base):
    """Ad model - represents a Meta Ad."""

    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String(50), nullable=False, unique=True, index=True)  # Meta ad ID
    ad_set_id = Column(Integer, ForeignKey("ad_sets.id"), nullable=False)
    creative_id = Column(Integer, ForeignKey("creatives.id"), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(
        SQLEnum(AdStatus, name="ad_status", create_type=True),
        nullable=False,
        default=AdStatus.ACTIVE
    )
    tracking_specs = Column(JSON, nullable=True)  # Conversion tracking specs
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    ad_set = relationship("AdSet", back_populates="ads")
    creative = relationship("Creative", back_populates="ads")
    ad_insights = relationship("AdInsight", back_populates="ad", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Ad {self.ad_id} - {self.name}>"
