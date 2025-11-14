"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.config import settings
from app.database import init_db
from app.domains.auto_shop.routers import customers, vehicles, work_orders, parts, mechanics, admin, service_jobs
from app.domains.marketing.routers import influencers, campaigns, promo_codes, influencer_payouts

# Initialize database tables
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## MockBizOps - Multi-Domain Mock API Platform

    A production-quality mock API service providing realistic business operations data across multiple domains
    for developers to use in testing and development.

    ### Auto Shop Domain
    - 🚗 **Customers**: Manage customer information and history
    - 🔧 **Vehicles**: Track vehicle details and service history
    - 📋 **Work Orders**: Comprehensive repair order management
    - 🛠️ **Mechanics**: Mechanic profiles and certifications
    - 📦 **Parts**: Parts inventory and pricing
    - 🔧 **Service Jobs**: Predefined service types and job codes

    ### Marketing Domain (Good Bogey Golf Apparel)
    - 👥 **Influencers**: Influencer/contractor profiles and social media data
    - 📢 **Campaigns**: Meta Marketing API-style ad campaigns
    - 🎟️ **Promo Codes**: Discount codes and usage tracking
    - 💰 **Influencer Payouts**: Commission and payment tracking
    - 📊 **Ad Insights**: Campaign performance metrics

    ### Authentication
    All endpoints require an API key. Include your API key in the `X-API-Key` header.

    Example:
    ```
    curl -H "X-API-Key: your-api-key-here" https://api.example.com/api/v1/customers
    ```

    ### Test API Keys
    For testing, use one of these pre-generated keys:
    - `test-key-1234567890`
    - `demo-key-abcdefghij`

    ### Admin Endpoints
    Admin endpoints (for managing API keys) require the admin API key set in your environment variables.

    ### Pagination
    List endpoints support pagination with `page` and `page_size` query parameters.
    Default page size is 20, maximum is 100.

    ### Filtering and Sorting
    Most list endpoints support filtering by relevant fields and sorting with `sort_by` and `order` parameters.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auto shop routers
app.include_router(customers.router, prefix=settings.API_V1_PREFIX)
app.include_router(vehicles.router, prefix=settings.API_V1_PREFIX)
app.include_router(work_orders.router, prefix=settings.API_V1_PREFIX)
app.include_router(parts.router, prefix=settings.API_V1_PREFIX)
app.include_router(mechanics.router, prefix=settings.API_V1_PREFIX)
app.include_router(service_jobs.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)

# Include marketing routers
app.include_router(influencers.router, prefix=f"{settings.API_V1_PREFIX}/marketing")
app.include_router(campaigns.router, prefix=f"{settings.API_V1_PREFIX}/marketing")
app.include_router(promo_codes.router, prefix=f"{settings.API_V1_PREFIX}/marketing")
app.include_router(influencer_payouts.router, prefix=f"{settings.API_V1_PREFIX}/marketing")


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    from app.database import SessionLocal, engine
    from sqlalchemy import text

    # Check database connection and tables
    try:
        db = SessionLocal()
        result = db.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]

        # Count records in each table
        counts = {}
        for table in tables:
            count_result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
            counts[table] = count_result.scalar()

        db.close()

        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "database": {
                "connected": True,
                "tables": tables,
                "record_counts": counts
            }
        }
    except Exception as e:
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "database": {
                "connected": False,
                "error": str(e)
            }
        }


@app.get(f"{settings.API_V1_PREFIX}/", include_in_schema=False)
async def api_root():
    """API root endpoint."""
    return {
        "message": "Car Repair Shop Mock API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
