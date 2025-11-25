"""
FMI 3.0 API routes for virtual prototype creation
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List, Optional
import logging
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from ..models.fmi_models import (
    FMUUploadResponse, FMUListResponse, FMUExportRequest, 
    FMUValidationResult, FMUSimulationConfig, FMUParameterSet
)
from fmi.parser import FMIParser
from fmi.validator import FMIValidator
from fmi.simulator import FMISimulator
from storage.file_manager import FileManager
from storage.database import get_db_session

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload", response_model=FMUUploadResponse)
async def upload_fmu(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    validate: bool = True
):
    """
    Upload and process an FMU file
    Supports FMI 1.0, 2.0, and 3.0 formats
    """
    if not file.filename.endswith('.fmu'):
        raise HTTPException(status_code=400, detail="File must be an FMU (.fmu extension)")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.fmu') as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = Path(temp_file.name)
        
        # Parse FMU
        parser = FMIParser()
        fmu_info = await parser.parse_fmu(temp_path)
        
        # Validate if requested
        validation_result = None
        if validate:
            validator = FMIValidator()
            validation_result = await validator.validate_fmu(temp_path)
        
        # Store FMU
        file_manager = FileManager()
        fmu_id = await file_manager.store_fmu(temp_path, file.filename, fmu_info)
        
        # Clean up temp file
        temp_path.unlink()
        
        # Prepare response
        response = FMUUploadResponse(
            fmu_id=fmu_id,
            filename=file.filename,
            file_size=file.size or 0,
            upload_time=fmu_info.generation_date_and_time or datetime.now(),
            info=fmu_info.info,
            variables=fmu_info.variables,
            validation_status="valid" if validation_result and validation_result.is_valid else "unknown",
            validation_messages=validation_result.errors + validation_result.warnings if validation_result else []
        )
        
        logger.info(f"Successfully uploaded FMU: {file.filename} (ID: {fmu_id})")
        return response
        
    except Exception as e:
        logger.error(f"Error uploading FMU {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process FMU: {str(e)}")

@router.get("/list", response_model=FMUListResponse)
async def list_fmus(
    skip: int = 0,
    limit: int = 100,
    filter_type: Optional[str] = None
):
    """
    List all uploaded FMUs with optional filtering
    """
    try:
        file_manager = FileManager()
        fmus = await file_manager.list_fmus(skip=skip, limit=limit, filter_type=filter_type)
        
        return FMUListResponse(
            fmus=fmus,
            total_count=len(fmus)
        )
        
    except Exception as e:
        logger.error(f"Error listing FMUs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list FMUs: {str(e)}")

@router.get("/{fmu_id}", response_model=FMUUploadResponse)
async def get_fmu(fmu_id: str):
    """
    Get detailed information about a specific FMU
    """
    try:
        file_manager = FileManager()
        fmu_info = await file_manager.get_fmu(fmu_id)
        
        if not fmu_info:
            raise HTTPException(status_code=404, detail="FMU not found")
        
        return fmu_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting FMU {fmu_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get FMU: {str(e)}")

@router.post("/{fmu_id}/validate", response_model=FMUValidationResult)
async def validate_fmu(fmu_id: str):
    """
    Validate an FMU against FMI standards
    """
    try:
        file_manager = FileManager()
        fmu_path = await file_manager.get_fmu_path(fmu_id)
        
        if not fmu_path:
            raise HTTPException(status_code=404, detail="FMU not found")
        
        validator = FMIValidator()
        result = await validator.validate_fmu(fmu_path)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating FMU {fmu_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to validate FMU: {str(e)}")

@router.post("/{fmu_id}/simulate")
async def simulate_fmu(
    fmu_id: str,
    config: FMUSimulationConfig,
    parameters: Optional[FMUParameterSet] = None
):
    """
    Run simulation of a single FMU
    """
    try:
        file_manager = FileManager()
        fmu_path = await file_manager.get_fmu_path(fmu_id)
        
        if not fmu_path:
            raise HTTPException(status_code=404, detail="FMU not found")
        
        simulator = FMISimulator()
        result = await simulator.simulate_single_fmu(
            fmu_path, config, parameters
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error simulating FMU {fmu_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to simulate FMU: {str(e)}")

@router.get("/{fmu_id}/download")
async def download_fmu(fmu_id: str):
    """
    Download an FMU file
    """
    try:
        file_manager = FileManager()
        fmu_path = await file_manager.get_fmu_path(fmu_id)
        fmu_info = await file_manager.get_fmu(fmu_id)
        
        if not fmu_path or not fmu_info:
            raise HTTPException(status_code=404, detail="FMU not found")
        
        return FileResponse(
            path=fmu_path,
            filename=fmu_info.filename,
            media_type="application/zip"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading FMU {fmu_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download FMU: {str(e)}")

@router.delete("/{fmu_id}")
async def delete_fmu(fmu_id: str):
    """
    Delete an FMU and its associated data
    """
    try:
        file_manager = FileManager()
        success = await file_manager.delete_fmu(fmu_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="FMU not found")
        
        return {"message": f"FMU {fmu_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting FMU {fmu_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete FMU: {str(e)}")

@router.post("/{fmu_id}/export")
async def export_fmu(fmu_id: str, request: FMUExportRequest):
    """
    Export FMU in different formats or for different platforms
    """
    try:
        file_manager = FileManager()
        fmu_path = await file_manager.get_fmu_path(fmu_id)
        
        if not fmu_path:
            raise HTTPException(status_code=404, detail="FMU not found")
        
        # For now, return the original FMU
        # In a full implementation, this would handle format conversion
        return FileResponse(
            path=fmu_path,
            filename=f"exported_{fmu_id}.fmu",
            media_type="application/zip"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting FMU {fmu_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to export FMU: {str(e)}")