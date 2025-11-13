"""Admin API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import get_db
from app.auth import get_admin_api_key
from app.models import APIKey
from app.schemas import APIKeyCreate, APIKeyResponse, APIKeyListResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/api-keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: APIKeyCreate,
    db: Session = Depends(get_db),
    admin_key: str = Depends(get_admin_api_key)
):
    """
    Create a new API key (admin only).

    Requires admin API key in X-API-Key header.
    """
    # Generate a new UUID-based API key
    new_key = str(uuid4())

    # Create the API key
    api_key = APIKey(
        key=new_key,
        name=key_data.name,
        is_active=True
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return api_key


@router.get("/api-keys", response_model=list[APIKeyListResponse])
async def list_api_keys(
    db: Session = Depends(get_db),
    admin_key: str = Depends(get_admin_api_key)
):
    """
    List all API keys (admin only).

    Requires admin API key in X-API-Key header.
    Note: The actual key values are not returned for security.
    """
    api_keys = db.query(APIKey).order_by(APIKey.created_at.desc()).all()
    return api_keys


@router.delete("/api-keys/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key: str,
    db: Session = Depends(get_db),
    admin_key: str = Depends(get_admin_api_key)
):
    """
    Revoke an API key (admin only).

    Requires admin API key in X-API-Key header.
    This sets the is_active flag to False rather than deleting the record.
    """
    api_key = db.query(APIKey).filter(APIKey.key == key).first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key not found"
        )

    # Deactivate the key
    api_key.is_active = False
    db.commit()

    return None


@router.post("/seed", status_code=status.HTTP_200_OK)
async def seed_database(
    db: Session = Depends(get_db),
    admin_key: str = Depends(get_admin_api_key)
):
    """
    Seed the database with mock data (admin only).

    Requires admin API key in X-API-Key header.
    This will populate the database with sample customers, vehicles, work orders, etc.
    """
    from app.seed_data import seed_database as run_seed

    try:
        # Run the seed function
        run_seed()

        return {
            "status": "success",
            "message": "Database seeded successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed database: {str(e)}"
        )
