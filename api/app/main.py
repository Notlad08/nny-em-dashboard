from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os

from app.core.config import settings
from app.core.db import engine, Base, get_db
from app.routes import ingest, incidents, units, timeline, external_data, health

# Create app
app = FastAPI(
    title="NNY Emergency Dashboard API",
    description="Real-time emergency communications monitoring system",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "database": "connected" if settings.DATABASE_URL else "not configured",
    }

# Include routes
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["Ingestion"])
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["Incidents"])
app.include_router(units.router, prefix="/api/v1/units", tags=["Units"])
app.include_router(timeline.router, prefix="/api/v1/timeline", tags=["Timeline"])
app.include_router(external_data.router, prefix="/api/v1/external", tags=["External Data"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "exception": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
