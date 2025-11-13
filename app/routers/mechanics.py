"""Mechanics API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

import math

from app.database import get_db
from app.auth import get_api_key
from app.models import Mechanic, WorkOrder, Vehicle, Customer, CertificationLevel
from app.schemas import (
    MechanicResponse,
    MechanicListResponse,
    WorkOrderListResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/mechanics", tags=["mechanics"])


@router.get("", response_model=PaginatedResponse[MechanicListResponse])
async def list_mechanics(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    certification_level: Optional[CertificationLevel] = Query(None, description="Filter by certification level"),
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    sort_by: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all mechanics with pagination and filtering."""
    query = db.query(Mechanic)

    # Apply filters
    if is_active is not None:
        query = query.filter(Mechanic.is_active == is_active)
    if certification_level:
        query = query.filter(Mechanic.certification_level == certification_level)
    if specialty:
        # Filter by specialty in JSONB array
        query = query.filter(Mechanic.specialties.contains([specialty]))

    # Apply sorting
    sort_column = getattr(Mechanic, sort_by, Mechanic.created_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Paginate
    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{mechanic_id}", response_model=MechanicResponse)
async def get_mechanic(
    mechanic_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific mechanic by ID."""
    mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()

    if not mechanic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mechanic with ID {mechanic_id} not found"
        )

    return mechanic


@router.get("/{mechanic_id}/work-orders", response_model=PaginatedResponse[WorkOrderListResponse])
async def get_mechanic_work_orders(
    mechanic_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get all work orders assigned to a specific mechanic."""
    # Check if mechanic exists
    mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
    if not mechanic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mechanic with ID {mechanic_id} not found"
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
        WorkOrder.assigned_mechanic_id == mechanic_id
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
