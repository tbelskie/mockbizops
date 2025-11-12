"""Customer API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.auth import get_api_key
from app.models import Customer, Vehicle, WorkOrder
from app.schemas import (
    CustomerResponse,
    CustomerListResponse,
    VehicleListResponse,
    WorkOrderListResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=PaginatedResponse[CustomerListResponse])
async def list_customers(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name, email, or phone"),
    state: Optional[str] = Query(None, description="Filter by state"),
    sort_by: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all customers with pagination and filtering."""
    query = db.query(Customer)

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Customer.first_name.ilike(search_term),
                Customer.last_name.ilike(search_term),
                Customer.email.ilike(search_term),
                Customer.phone.ilike(search_term)
            )
        )

    # Apply state filter
    if state:
        query = query.filter(Customer.state == state.upper())

    # Apply sorting
    sort_column = getattr(Customer, sort_by, Customer.created_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Paginate
    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific customer by ID."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )

    return customer


@router.get("/{customer_id}/vehicles", response_model=PaginatedResponse[VehicleListResponse])
async def get_customer_vehicles(
    customer_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get all vehicles for a specific customer."""
    # Check if customer exists
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )

    query = db.query(Vehicle).filter(Vehicle.customer_id == customer_id)
    query = query.order_by(Vehicle.created_at.desc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{customer_id}/work-orders", response_model=PaginatedResponse[WorkOrderListResponse])
async def get_customer_work_orders(
    customer_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get all work orders for a specific customer."""
    # Check if customer exists
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
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
        WorkOrder.customer_id == customer_id
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

    import math
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    return create_paginated_response(items, total, page, page_size, total_pages)
