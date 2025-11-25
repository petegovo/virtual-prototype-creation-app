"""
Virtual Prototype Creation App - Main FastAPI Application
Supports FMI 3.0 and SSP 2.0 import/export for SystemC, Simulink, and Modelica IP
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import logging
from pathlib import Path

from api.routes import fmi, ssp, simulation, projects
from storage.database import init_database
from storage.file_manager import FileManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Virtual Prototype Creation App")
    
    # Initialize database
    await init_database()
    
    # Initialize file manager
    FileManager.initialize()
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")

# Create FastAPI application
app = FastAPI(
    title="Virtual Prototype Creation App",
    description="Web-based virtual prototyping with FMI 3.0 and SSP 2.0 support",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(fmi.router, prefix="/api/fmi", tags=["FMI"])
app.include_router(ssp.router, prefix="/api/ssp", tags=["SSP"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["Simulation"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])

# Mount static files for uploads
uploads_path = Path("uploads")
uploads_path.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Virtual Prototype Creation App API",
        "version": "1.0.0",
        "features": [
            "FMI 3.0 import/export",
            "SSP 2.0 system structure",
            "Multi-domain co-simulation",
            "SystemC/Simulink/Modelica integration"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "virtual-prototype-api"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )