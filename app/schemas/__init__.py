"""Schemas package."""
from app.schemas.common import PaginatedResponse
from app.schemas.customer import CustomerResponse, CustomerListResponse
from app.schemas.vehicle import VehicleResponse, VehicleListResponse, VehicleWithCustomer
from app.schemas.mechanic import MechanicResponse, MechanicListResponse
from app.schemas.part import PartResponse, PartListResponse
from app.schemas.labor_item import LaborItemResponse, LaborItemWithMechanic
from app.schemas.work_order import (
    WorkOrderResponse,
    WorkOrderListResponse,
    WorkOrderDetailResponse,
    WorkOrderStatsResponse
)
from app.schemas.api_key import APIKeyCreate, APIKeyResponse, APIKeyListResponse
from app.schemas.service_job import (
    ServiceJobResponse,
    ServiceJobListResponse,
    WorkOrderServiceJobResponse
)
from app.schemas.upsell import (
    UpsellResponse,
    UpsellListResponse,
    UpsellCreate,
    UpsellUpdateStatus
)

__all__ = [
    "PaginatedResponse",
    "CustomerResponse",
    "CustomerListResponse",
    "VehicleResponse",
    "VehicleListResponse",
    "VehicleWithCustomer",
    "MechanicResponse",
    "MechanicListResponse",
    "PartResponse",
    "PartListResponse",
    "LaborItemResponse",
    "LaborItemWithMechanic",
    "WorkOrderResponse",
    "WorkOrderListResponse",
    "WorkOrderDetailResponse",
    "WorkOrderStatsResponse",
    "APIKeyCreate",
    "APIKeyResponse",
    "APIKeyListResponse",
    "ServiceJobResponse",
    "ServiceJobListResponse",
    "WorkOrderServiceJobResponse",
    "UpsellResponse",
    "UpsellListResponse",
    "UpsellCreate",
    "UpsellUpdateStatus",
]
