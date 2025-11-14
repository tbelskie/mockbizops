"""Work order schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

from decimal import Decimal
from app.domains.auto_shop.models.work_order import (
    WorkOrderStatus,
    WorkOrderPriority,
    PaymentStatus,
    PaymentMethod,
    WorkOrderType
)
from app.domains.auto_shop.schemas.part import PartResponse
from app.domains.auto_shop.schemas.labor_item import LaborItemResponse


class WorkOrderBase(BaseModel):
    """Base work order schema."""
    description: str = Field(..., min_length=1)
    customer_concern: str = Field(..., min_length=1)
    diagnosis: Optional[str] = None
    priority: WorkOrderPriority = WorkOrderPriority.NORMAL
    odometer_in: int = Field(..., ge=0)


class WorkOrderResponse(BaseModel):
    """Work order response schema."""
    id: int
    work_order_number: str
    vehicle_id: int
    customer_id: int
    assigned_mechanic_id: Optional[int]
    status: WorkOrderStatus
    priority: WorkOrderPriority
    work_order_type: WorkOrderType
    description: str
    customer_concern: str
    diagnosis: Optional[str]
    estimated_completion: Optional[datetime]
    actual_completion: Optional[datetime]
    odometer_in: int
    odometer_out: Optional[int]
    labor_hours: Optional[Decimal]
    service_job_ids: Optional[List[int]]
    additional_service_job_ids: Optional[List[int]]
    subtotal_parts: Decimal
    subtotal_labor: Decimal
    service_jobs_cost: Decimal
    additional_jobs_cost: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    payment_status: PaymentStatus
    payment_method: Optional[PaymentMethod]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkOrderListResponse(BaseModel):
    """Work order response for list views - includes all fields."""
    id: int
    work_order_number: str
    vehicle_id: int
    customer_id: int
    assigned_mechanic_id: Optional[int]
    status: WorkOrderStatus
    priority: WorkOrderPriority
    work_order_type: WorkOrderType
    description: str
    customer_concern: str
    diagnosis: Optional[str]
    estimated_completion: Optional[datetime]
    actual_completion: Optional[datetime]
    odometer_in: int
    odometer_out: Optional[int]
    labor_hours: Optional[Decimal]
    service_job_ids: Optional[List[int]]
    additional_service_job_ids: Optional[List[int]]
    subtotal_parts: Decimal
    subtotal_labor: Decimal
    service_jobs_cost: Decimal
    additional_jobs_cost: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    payment_status: PaymentStatus
    payment_method: Optional[PaymentMethod]
    created_at: datetime
    updated_at: datetime
    # Joined fields for convenience
    vehicle_year: int
    vehicle_make: str
    vehicle_model: str
    customer_first_name: str
    customer_last_name: str

    model_config = ConfigDict(from_attributes=True)


class WorkOrderDetailResponse(WorkOrderResponse):
    """Detailed work order response with parts and labor."""
    parts: List[PartResponse] = []
    labor_items: List[LaborItemResponse] = []
    # Customer info
    customer_first_name: str
    customer_last_name: str
    customer_email: str
    customer_phone: str
    # Vehicle info
    vehicle_year: int
    vehicle_make: str
    vehicle_model: str
    vehicle_vin: str
    # Mechanic info
    mechanic_first_name: Optional[str] = None
    mechanic_last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class WorkOrderStatsResponse(BaseModel):
    """Work order statistics response."""
    total_orders: int
    pending_orders: int
    in_progress_orders: int
    completed_orders: int
    cancelled_orders: int
    total_revenue: Decimal
    unpaid_amount: Decimal
    average_order_value: Decimal
