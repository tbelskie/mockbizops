"""Work order API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
import math

from app.database import get_db
from app.auth import get_api_key
from app.models import WorkOrder, Vehicle, Customer, Mechanic, Part, LaborItem, WorkOrderStatus, WorkOrderPriority, PaymentStatus
from app.schemas import (
    WorkOrderResponse,
    WorkOrderListResponse,
    WorkOrderDetailResponse,
    WorkOrderStatsResponse,
    PartResponse,
    LaborItemResponse,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


@router.get("", response_model=PaginatedResponse[WorkOrderListResponse])
async def list_work_orders(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[WorkOrderStatus] = Query(None, description="Filter by status"),
    priority: Optional[WorkOrderPriority] = Query(None, description="Filter by priority"),
    payment_status: Optional[PaymentStatus] = Query(None, description="Filter by payment status"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    sort_by: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all work orders with pagination and filtering."""
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
    )

    # Apply filters
    if status:
        query = query.filter(WorkOrder.status == status)
    if priority:
        query = query.filter(WorkOrder.priority == priority)
    if payment_status:
        query = query.filter(WorkOrder.payment_status == payment_status)
    if start_date:
        query = query.filter(WorkOrder.created_at >= start_date)
    if end_date:
        query = query.filter(WorkOrder.created_at <= end_date)

    # Apply sorting
    sort_column = getattr(WorkOrder, sort_by, WorkOrder.created_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

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


@router.get("/stats", response_model=WorkOrderStatsResponse)
async def get_work_order_stats(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get summary statistics for work orders."""
    # Count by status
    total_orders = db.query(func.count(WorkOrder.id)).scalar()
    pending_orders = db.query(func.count(WorkOrder.id)).filter(
        WorkOrder.status == WorkOrderStatus.PENDING
    ).scalar()
    in_progress_orders = db.query(func.count(WorkOrder.id)).filter(
        WorkOrder.status == WorkOrderStatus.IN_PROGRESS
    ).scalar()
    completed_orders = db.query(func.count(WorkOrder.id)).filter(
        WorkOrder.status == WorkOrderStatus.COMPLETED
    ).scalar()
    cancelled_orders = db.query(func.count(WorkOrder.id)).filter(
        WorkOrder.status == WorkOrderStatus.CANCELLED
    ).scalar()

    # Revenue calculations
    total_revenue = db.query(func.sum(WorkOrder.total_amount)).filter(
        WorkOrder.payment_status == PaymentStatus.PAID
    ).scalar() or Decimal("0.00")

    unpaid_amount = db.query(func.sum(WorkOrder.total_amount)).filter(
        WorkOrder.payment_status == PaymentStatus.UNPAID
    ).scalar() or Decimal("0.00")

    # Average order value
    average_order_value = db.query(func.avg(WorkOrder.total_amount)).scalar() or Decimal("0.00")

    return WorkOrderStatsResponse(
        total_orders=total_orders,
        pending_orders=pending_orders,
        in_progress_orders=in_progress_orders,
        completed_orders=completed_orders,
        cancelled_orders=cancelled_orders,
        total_revenue=total_revenue,
        unpaid_amount=unpaid_amount,
        average_order_value=average_order_value
    )


@router.get("/{work_order_id}", response_model=WorkOrderDetailResponse)
async def get_work_order(
    work_order_id: UUID,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get detailed work order information including parts and labor."""
    # Query with joins
    result = db.query(
        WorkOrder,
        Vehicle.year.label("vehicle_year"),
        Vehicle.make.label("vehicle_make"),
        Vehicle.model.label("vehicle_model"),
        Vehicle.vin.label("vehicle_vin"),
        Customer.first_name.label("customer_first_name"),
        Customer.last_name.label("customer_last_name"),
        Customer.email.label("customer_email"),
        Customer.phone.label("customer_phone"),
        Mechanic.first_name.label("mechanic_first_name"),
        Mechanic.last_name.label("mechanic_last_name")
    ).join(
        Vehicle, WorkOrder.vehicle_id == Vehicle.id
    ).join(
        Customer, WorkOrder.customer_id == Customer.id
    ).outerjoin(
        Mechanic, WorkOrder.assigned_mechanic_id == Mechanic.id
    ).filter(
        WorkOrder.id == work_order_id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID {work_order_id} not found"
        )

    work_order = result[0]

    # Get parts and labor
    parts = db.query(Part).filter(Part.work_order_id == work_order_id).all()
    labor_items = db.query(LaborItem).filter(LaborItem.work_order_id == work_order_id).all()

    # Construct response
    return WorkOrderDetailResponse(
        id=work_order.id,
        work_order_number=work_order.work_order_number,
        vehicle_id=work_order.vehicle_id,
        customer_id=work_order.customer_id,
        assigned_mechanic_id=work_order.assigned_mechanic_id,
        status=work_order.status,
        priority=work_order.priority,
        description=work_order.description,
        customer_concern=work_order.customer_concern,
        diagnosis=work_order.diagnosis,
        estimated_completion=work_order.estimated_completion,
        actual_completion=work_order.actual_completion,
        odometer_in=work_order.odometer_in,
        odometer_out=work_order.odometer_out,
        subtotal_parts=work_order.subtotal_parts,
        subtotal_labor=work_order.subtotal_labor,
        tax_rate=work_order.tax_rate,
        tax_amount=work_order.tax_amount,
        total_amount=work_order.total_amount,
        payment_status=work_order.payment_status,
        payment_method=work_order.payment_method,
        created_at=work_order.created_at,
        updated_at=work_order.updated_at,
        parts=parts,
        labor_items=labor_items,
        customer_first_name=result.customer_first_name,
        customer_last_name=result.customer_last_name,
        customer_email=result.customer_email,
        customer_phone=result.customer_phone,
        vehicle_year=result.vehicle_year,
        vehicle_make=result.vehicle_make,
        vehicle_model=result.vehicle_model,
        vehicle_vin=result.vehicle_vin,
        mechanic_first_name=result.mechanic_first_name,
        mechanic_last_name=result.mechanic_last_name
    )


@router.get("/{work_order_id}/parts", response_model=PaginatedResponse[PartResponse])
async def get_work_order_parts(
    work_order_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get all parts for a specific work order."""
    # Check if work order exists
    work_order = db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()
    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID {work_order_id} not found"
        )

    query = db.query(Part).filter(Part.work_order_id == work_order_id)
    query = query.order_by(Part.created_at.asc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{work_order_id}/labor", response_model=PaginatedResponse[LaborItemResponse])
async def get_work_order_labor(
    work_order_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get all labor items for a specific work order."""
    # Check if work order exists
    work_order = db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()
    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID {work_order_id} not found"
        )

    query = db.query(LaborItem).filter(LaborItem.work_order_id == work_order_id)
    query = query.order_by(LaborItem.created_at.asc())

    items, total, page, page_size, total_pages = paginate(query, page, page_size)

    return create_paginated_response(items, total, page, page_size, total_pages)
