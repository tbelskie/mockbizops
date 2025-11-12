"""API key authentication."""
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.sql import func
from app.database import get_db
from app.models.api_key import APIKey
from app.config import settings

# API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
) -> APIKey:
    """
    Validate API key and return the APIKey object.

    Args:
        api_key: API key from request header
        db: Database session

    Returns:
        APIKey object if valid

    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Check if it's the admin key
    if api_key == settings.ADMIN_API_KEY:
        # Return a mock APIKey object for admin
        admin_key = APIKey(
            name="Admin Key",
            key=settings.ADMIN_API_KEY,
            is_active=True
        )
        return admin_key

    # Look up the key in the database
    db_api_key = db.query(APIKey).filter(
        APIKey.key == api_key,
        APIKey.is_active == True
    ).first()

    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Update last_used_at timestamp
    db.execute(
        update(APIKey)
        .where(APIKey.id == db_api_key.id)
        .values(last_used_at=func.now())
    )
    db.commit()

    return db_api_key


async def get_admin_api_key(
    api_key: str = Security(api_key_header)
) -> str:
    """
    Validate that the API key is the admin key.

    Args:
        api_key: API key from request header

    Returns:
        Admin API key if valid

    Raises:
        HTTPException: If API key is not the admin key
    """
    if not api_key or api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin API key required for this operation",
        )

    return api_key
