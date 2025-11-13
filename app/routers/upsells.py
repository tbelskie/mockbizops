"""Upsells API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from decimal import Decimal

from app.database import get_db
from app.auth import get_api_key
from app.models import Upsell, UpsellStatus, WorkOrder, Mechanic
from app.schemas import (
    UpsellResponse,
    UpsellListResponse,
    UpsellCreate,
    UpsellUpdateStatus,
    MechanicCommissionSummary,
    PaginatedResponse
)
from app.utils import paginate, create_paginated_response

router = APIRouter(prefix="/upsells", tags=["upsells"])


@router.get("", response_model=PaginatedResponse[UpsellListResponse])
async def list_upsells(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[UpsellStatus] = Query(None, description="Filter by status"),
    work_order_id: Optional[int] = Query(None, description="Filter by work order"),
    mechanic_id: Optional[int] = Query(None, description="Filter by mechanic"),
    sort_by: str = Query("proposed_at", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """List all upsells with pagination and filtering."""
    query = db.query(
        Upsell,
        WorkOrder.work_order_number.label("work_order_number"),
        Mechanic.first_name.label("recommended_by_first_name"),
        Mechanic.last_name.label("recommended_by_last_name")
    ).join(
        WorkOrder, Upsell.work_order_id == WorkOrder.id
    ).join(
        Mechanic, Upsell.recommended_by_mechanic_id == Mechanic.id
    )

    # Apply filters
    if status:
        query = query.filter(Upsell.status == status)
    if work_order_id:
        query = query.filter(Upsell.work_order_id == work_order_id)
    if mechanic_id:
        query = query.filter(Upsell.recommended_by_mechanic_id == mechanic_id)

    # Apply sorting
    sort_column = getattr(Upsell, sort_by, Upsell.proposed_at)
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
        upsell = row[0]
        items.append(UpsellListResponse(
            id=upsell.id,
            work_order_id=upsell.work_order_id,
            work_order_number=row.work_order_number,
            recommended_by_first_name=row.recommended_by_first_name,
            recommended_by_last_name=row.recommended_by_last_name,
            description=upsell.description,
            estimated_amount=upsell.estimated_amount,
            actual_amount=upsell.actual_amount,
            commission_amount=upsell.commission_amount,
            status=upsell.status,
            proposed_at=upsell.proposed_at
        ))

    import math
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    return create_paginated_response(items, total, page, page_size, total_pages)


@router.get("/{upsell_id}", response_model=UpsellResponse)
async def get_upsell(
    upsell_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific upsell by ID."""
    upsell = db.query(Upsell).filter(Upsell.id == upsell_id).first()

    if not upsell:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Upsell with ID {upsell_id} not found"
        )

    return upsell


@router.post("", response_model=UpsellResponse, status_code=status.HTTP_201_CREATED)
async def create_upsell(
    upsell_data: UpsellCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Create a new upsell."""
    # Verify work order exists
    work_order = db.query(WorkOrder).filter(WorkOrder.id == upsell_data.work_order_id).first()
    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID {upsell_data.work_order_id} not found"
        )

    # Verify mechanic exists
    mechanic = db.query(Mechanic).filter(Mechanic.id == upsell_data.recommended_by_mechanic_id).first()
    if not mechanic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mechanic with ID {upsell_data.recommended_by_mechanic_id} not found"
        )

    upsell = Upsell(
        work_order_id=upsell_data.work_order_id,
        recommended_by_mechanic_id=upsell_data.recommended_by_mechanic_id,
        description=upsell_data.description,
        reason=upsell_data.reason,
        estimated_amount=upsell_data.estimated_amount,
        commission_rate=upsell_data.commission_rate,
        status=UpsellStatus.PROPOSED
    )

    db.add(upsell)
    db.commit()
    db.refresh(upsell)

    return upsell


@router.patch("/{upsell_id}/status", response_model=UpsellResponse)
async def update_upsell_status(
    upsell_id: int,
    update_data: UpsellUpdateStatus,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Update upsell status (approve, decline, complete)."""
    upsell = db.query(Upsell).filter(Upsell.id == upsell_id).first()

    if not upsell:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Upsell with ID {upsell_id} not found"
        )

    # Update status
    upsell.status = update_data.status

    # Update timestamps based on status
    from datetime import datetime
    if update_data.status == UpsellStatus.APPROVED and not upsell.approved_at:
        upsell.approved_at = datetime.now()
    elif update_data.status == UpsellStatus.COMPLETED and not upsell.completed_at:
        upsell.completed_at = datetime.now()

    # Update actual amount if provided
    if update_data.actual_amount is not None:
        upsell.actual_amount = update_data.actual_amount

    # Update notes if provided
    if update_data.notes is not None:
        upsell.notes = update_data.notes

    # Calculate commission
    upsell.calculate_commission()

    db.commit()
    db.refresh(upsell)

    return upsell


@router.get("/mechanic/{mechanic_id}/commission-summary", response_model=MechanicCommissionSummary)
async def get_mechanic_commission_summary(
    mechanic_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get commission summary for a mechanic."""
    mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()

    if not mechanic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mechanic with ID {mechanic_id} not found"
        )

    # Get upsell statistics
    total_proposed = db.query(func.count(Upsell.id)).filter(
        Upsell.recommended_by_mechanic_id == mechanic_id
    ).scalar()

    total_approved = db.query(func.count(Upsell.id)).filter(
        Upsell.recommended_by_mechanic_id == mechanic_id,
        Upsell.status.in_([UpsellStatus.APPROVED, UpsellStatus.COMPLETED])
    ).scalar()

    total_completed = db.query(func.count(Upsell.id)).filter(
        Upsell.recommended_by_mechanic_id == mechanic_id,
        Upsell.status == UpsellStatus.COMPLETED
    ).scalar()

    # Calculate commissions
    total_commission = db.query(func.coalesce(func.sum(Upsell.commission_amount), 0)).filter(
        Upsell.recommended_by_mechanic_id == mechanic_id,
        Upsell.status == UpsellStatus.COMPLETED
    ).scalar()

    pending_commission = db.query(func.coalesce(func.sum(Upsell.commission_amount), 0)).filter(
        Upsell.recommended_by_mechanic_id == mechanic_id,
        Upsell.status == UpsellStatus.APPROVED
    ).scalar()

    # Calculate approval rate
    approval_rate = Decimal("0")
    if total_proposed > 0:
        approval_rate = Decimal(str((total_approved / total_proposed) * 100))

    return MechanicCommissionSummary(
        mechanic_id=mechanic.id,
        mechanic_first_name=mechanic.first_name,
        mechanic_last_name=mechanic.last_name,
        total_upsells_proposed=total_proposed,
        total_upsells_approved=total_approved,
        total_upsells_completed=total_completed,
        approval_rate=round(approval_rate, 2),
        total_commission_earned=Decimal(str(total_commission)),
        pending_commission=Decimal(str(pending_commission))
    )
