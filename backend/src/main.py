"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import reports
from src.config import settings
from src.middleware.security import setup_security_headers

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Growth Force Reporting Agent API")
    yield
    # Shutdown
    logger.info("Shutting down Growth Force Reporting Agent API")


# Create FastAPI app
app = FastAPI(
    title="Growth Force Reporting Agent API",
    description="AI-powered reporting agent for BigQuery analysis",
    version="0.1.0",
    lifespan=lifespan,
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Setup security headers
setup_security_headers(app)

# Include routers
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

# Add BigQuery router for testing (remove in production)
if settings.environment == "development":
    from src.api import bigquery
    app.include_router(bigquery.router, prefix="/api/bigquery", tags=["bigquery"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Growth Force Reporting Agent API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development",
    )