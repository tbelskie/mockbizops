"""Ad account model."""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class AdAccountStatus(str, enum.Enum):
    """Ad account status."""
    ACTIVE = "active"
    DISABLED = "disabled"


class AdAccount(Base):
    """Ad account model - represents a Meta Ads account."""

    __tablename__ = "ad_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(50), nullable=False, unique=True, index=True)  # Meta account ID
    name = Column(String(255), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")  # ISO 4217
    timezone = Column(String(50), nullable=False, default="America/New_York")
    status = Column(
        SQLEnum(AdAccountStatus, name="ad_account_status", create_type=True),
        nullable=False,
        default=AdAccountStatus.ACTIVE
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    campaigns = relationship("Campaign", back_populates="ad_account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AdAccount {self.account_id} - {self.name}>"
