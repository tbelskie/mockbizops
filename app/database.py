"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create auto shop database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create session factory for auto shop
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create marketing database engine
marketing_engine = create_engine(
    settings.MARKETING_DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create session factory for marketing
MarketingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=marketing_engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get auto shop database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_marketing_db():
    """Dependency to get marketing database session."""
    db = MarketingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize auto shop database tables."""
    Base.metadata.create_all(bind=engine)


def init_marketing_db():
    """Initialize marketing database tables."""
    Base.metadata.create_all(bind=marketing_engine)
