from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.database import engine
from app.database.base import Base

# Import all routers to register them
from app.routers import (
    user,
    department,
    asset_category,
    asset,
    allocation,
    booking,
    maintenance,
    dashboard
)

# Create SQLite database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set CORS middleware (essential for independent React frontend consumption)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production envs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(user.router, prefix=settings.API_V1_STR)
app.include_router(department.router, prefix=settings.API_V1_STR)
app.include_router(asset_category.router, prefix=settings.API_V1_STR)
app.include_router(asset.router, prefix=settings.API_V1_STR)
app.include_router(allocation.router, prefix=settings.API_V1_STR)
app.include_router(booking.router, prefix=settings.API_V1_STR)
app.include_router(maintenance.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "success": True,
        "message": "AssetFlow Enterprise Resource Management API is live.",
        "docs": "/docs"
    }
