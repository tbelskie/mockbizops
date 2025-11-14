"""Ad insight model."""
from sqlalchemy import Column, Integer, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AdInsight(Base):
    """Ad insight model - represents performance metrics for ads."""

    __tablename__ = "ad_insights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey("ads.id"), nullable=False)
    date_start = Column(Date, nullable=False)
    date_stop = Column(Date, nullable=False)
    impressions = Column(Integer, nullable=False, default=0)
    clicks = Column(Integer, nullable=False, default=0)
    spend = Column(Numeric(10, 2), nullable=False, default=0.00)
    reach = Column(Integer, nullable=False, default=0)
    frequency = Column(Numeric(5, 2), nullable=True)  # Average times shown per person
    cpc = Column(Numeric(10, 2), nullable=True)  # Cost per click
    cpm = Column(Numeric(10, 2), nullable=True)  # Cost per 1000 impressions
    ctr = Column(Numeric(5, 2), nullable=True)  # Click-through rate (%)
    conversions = Column(Integer, nullable=False, default=0)
    conversion_value = Column(Numeric(10, 2), nullable=False, default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    ad = relationship("Ad", back_populates="ad_insights")

    def __repr__(self):
        return f"<AdInsight ad_id={self.ad_id} {self.date_start} to {self.date_stop}>"
