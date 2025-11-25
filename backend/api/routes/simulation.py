"""
Simulation API routes for virtual prototype creation
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/start")
async def start_simulation(config: Dict[str, Any]):
    """Start a simulation"""
    # Placeholder implementation
    raise HTTPException(status_code=501, detail="Simulation not yet implemented")

@router.get("/status")
async def get_simulation_status():
    """Get simulation status"""
    return {"status": "stopped", "progress": 0.0}