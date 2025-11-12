"""Vehicle API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import math

from app.database import get_db
from app.auth import get_api_key
from app.models import Vehicle, Customer, WorkOrder
from app.schemas import (
    VehicleResponse,
    VehicleListResponse,
    WorkOrderListResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("", response_model=PaginatedResponse[VehicleListResponse])
async def list_vehicles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    make: Optional[str] = Query(None, description="Filter by make"),
    model: Optional[str] = Query(None, description="Filter by model"),
    year: Optional[int] = Query(None, description="Filter by year"),
    sort_by: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all vehicles with pagination and filtering."""
    query = db.query(Vehicle)

    # Apply filters
    if make:
        query = query.filter(Vehicle.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if year:
        query = query.filter(Vehicle.year == year)

    # Apply sorting
    sort_column = getattr(Vehicle, sort_by, Vehicle.created_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Paginate
    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific vehicle by ID."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {vehicle_id} not found"
        )

    return vehicle


@router.get("/{vehicle_id}/work-orders", response_model=PaginatedResponse[WorkOrderListResponse])
async def get_vehicle_work_orders(
    vehicle_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get service history (work orders) for a specific vehicle."""
    # Check if vehicle exists
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {vehicle_id} not found"
        )

    query = db.query(
        WorkOrder,
        Vehicle.year.label("vehicle_year"),
        Vehicle.make.label("vehicle_make"),
        Vehicle.model.label("vehicle_model"),
        Customer.first_name.label("customer_first_name"),
        Customer.last_name.label("customer_last_name")
    ).join(
        Vehicle, WorkOrder.vehicle_id == Vehicle.id
    ).join(
        Customer, WorkOrder.customer_id == Customer.id
    ).filter(
        WorkOrder.vehicle_id == vehicle_id
    ).order_by(
        WorkOrder.created_at.desc()
    )

    # Manually paginate for joined query
    total = query.count()
    items_raw = query.offset((page - 1) * page_size).limit(page_size).all()

    # Convert to response schema
    items = []
    for row in items_raw:
        work_order = row[0]
        items.append(WorkOrderListResponse(
            id=work_order.id,
            work_order_number=work_order.work_order_number,
            vehicle_year=row.vehicle_year,
            vehicle_make=row.vehicle_make,
            vehicle_model=row.vehicle_model,
            customer_first_name=row.customer_first_name,
            customer_last_name=row.customer_last_name,
            status=work_order.status,
            priority=work_order.priority,
            total_amount=work_order.total_amount,
            payment_status=work_order.payment_status,
            created_at=work_order.created_at
        ))

    total_pages = math.ceil(total / page_size) if total > 0 else 1

    return create_paginated_response(items, total, page, page_size, total_pages)
