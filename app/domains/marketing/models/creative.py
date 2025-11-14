"""Creative model."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Creative(Base):
    """Creative model - represents ad creative (images, videos, copy)."""

    __tablename__ = "creatives"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creative_id = Column(String(50), nullable=False, unique=True, index=True)  # Meta creative ID
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)  # Ad copy
    image_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    call_to_action = Column(String(50), nullable=True)  # e.g., "shop_now", "learn_more"
    link_url = Column(String(500), nullable=True)
    instagram_permalink_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    ads = relationship("Ad", back_populates="creative")

    def __repr__(self):
        return f"<Creative {self.creative_id} - {self.name}>"
