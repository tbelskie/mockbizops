"""Schemas package."""
from app.domains.auto_shop.schemas.common import PaginatedResponse
from app.domains.auto_shop.schemas.customer import CustomerResponse, CustomerListResponse
from app.domains.auto_shop.schemas.vehicle import VehicleResponse, VehicleListResponse, VehicleWithCustomer
from app.domains.auto_shop.schemas.mechanic import MechanicResponse, MechanicListResponse
from app.domains.auto_shop.schemas.part import PartResponse, PartListResponse
from app.domains.auto_shop.schemas.labor_item import LaborItemResponse, LaborItemWithMechanic
from app.domains.auto_shop.schemas.work_order import (
    WorkOrderResponse,
    WorkOrderListResponse,
    WorkOrderDetailResponse,
    WorkOrderStatsResponse
)
from app.domains.auto_shop.schemas.api_key import APIKeyCreate, APIKeyResponse, APIKeyListResponse
from app.domains.auto_shop.schemas.service_job import (
    ServiceJobResponse,
    ServiceJobListResponse
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
]
