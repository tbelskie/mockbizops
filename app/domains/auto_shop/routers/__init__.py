"""Routers package."""
from app.domains.auto_shop.routers import customers, vehicles, work_orders, parts, mechanics, admin, service_jobs

__all__ = [
    "customers",
    "vehicles",
    "work_orders",
    "parts",
    "mechanics",
    "admin",
    "service_jobs",
]
