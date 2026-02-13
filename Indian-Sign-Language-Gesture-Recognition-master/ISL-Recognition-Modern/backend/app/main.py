"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db
from app.routers import gesture, audio

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Modern Indian Sign Language Recognition System with bidirectional translation",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(gesture.router, prefix="/api/gesture", tags=["Gesture Recognition"])
app.include_router(audio.router, prefix="/api/audio", tags=["Audio Processing"])

# Mount static files
import os
from pathlib import Path
base_path = Path(__file__).parent.parent # backend/
data_path = base_path / "data"
os.makedirs(data_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(data_path)), name="static")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ISL Recognition API",
        "version": settings.app_version,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
