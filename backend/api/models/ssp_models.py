"""
Pydantic models for SSP 2.0 API endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime

class SSPVersion(str, Enum):
    """SSP version enumeration"""
    SSP_1_0 = "1.0"
    SSP_2_0 = "2.0"

class ComponentType(str, Enum):
    """SSP component types"""
    FMU = "application/x-fmu-sharedlibrary"
    MODELICA = "application/x-modelica-fmu"
    SYSTEMC = "application/x-systemc-fmu"
    SIMULINK = "application/x-simulink-fmu"
    ABSTRACT = "application/x-ssp-abstract"

class ConnectorKind(str, Enum):
    """SSP connector kinds"""
    INPUT = "input"
    OUTPUT = "output"
    PARAMETER = "parameter"
    CALCULATED_PARAMETER = "calculatedParameter"

class SSPConnector(BaseModel):
    """SSP connector definition"""
    name: str
    kind: ConnectorKind
    type: str  # Real, Integer, Boolean, String, etc.
    unit: Optional[str] = None
    description: Optional[str] = None
    dimensions: Optional[List[int]] = None  # SSP 2.0 arrays

class SSPComponent(BaseModel):
    """SSP component definition"""
    name: str
    type: ComponentType
    source: Optional[str] = None  # Path to FMU or model file
    description: Optional[str] = None
    connectors: List[SSPConnector] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    position: Optional[Dict[str, float]] = None  # x, y coordinates for UI

class SSPConnection(BaseModel):
    """SSP connection between components"""
    start_element: str  # component.connector
    end_element: str    # component.connector
    description: Optional[str] = None
    connection_type: str = "signal"  # signal, bus, etc.

class SSPParameterBinding(BaseModel):
    """SSP parameter binding"""
    parameter: str  # component.parameter
    value: Union[float, int, bool, str]
    unit: Optional[str] = None

class SSPSystem(BaseModel):
    """SSP system definition"""
    name: str
    description: Optional[str] = None
    components: List[SSPComponent] = Field(default_factory=list)
    connections: List[SSPConnection] = Field(default_factory=list)
    parameter_bindings: List[SSPParameterBinding] = Field(default_factory=list)
    
class SSPMetadata(BaseModel):
    """SSP metadata"""
    name: str
    description: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = None
    copyright: Optional[str] = None
    license: Optional[str] = None
    generation_tool: Optional[str] = None
    generation_date_and_time: Optional[datetime] = None
    file_version: SSPVersion = SSPVersion.SSP_2_0

class SSPPackage(BaseModel):
    """Complete SSP package"""
    metadata: SSPMetadata
    system: SSPSystem
    resources: Dict[str, str] = Field(default_factory=dict)  # filename -> content_type

class SSPUploadResponse(BaseModel):
    """Response model for SSP upload"""
    ssp_id: str
    filename: str
    file_size: int
    upload_time: datetime
    package: SSPPackage
    validation_status: str
    validation_messages: List[str] = Field(default_factory=list)

class SSPListResponse(BaseModel):
    """Response model for SSP list"""
    packages: List[SSPUploadResponse]
    total_count: int

class SSPExportRequest(BaseModel):
    """Request model for SSP export"""
    ssp_id: str
    export_version: SSPVersion = SSPVersion.SSP_2_0
    include_resources: bool = True
    compression_level: int = 6

class SSPValidationResult(BaseModel):
    """SSP validation result"""
    is_valid: bool
    ssp_version: SSPVersion
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    info_messages: List[str] = Field(default_factory=list)

class SSPSystemComposition(BaseModel):
    """SSP system composition request"""
    name: str
    description: Optional[str] = None
    components: List[Dict[str, Any]]  # Component configurations
    connections: List[Dict[str, str]]  # Connection specifications
    parameters: Dict[str, Any] = Field(default_factory=dict)

class SSPArchitecture(BaseModel):
    """SSP 2.0 architectural specification"""
    name: str
    description: Optional[str] = None
    interfaces: List[SSPConnector] = Field(default_factory=list)
    requirements: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    traceability: Dict[str, Any] = Field(default_factory=dict)

class SSPTraceability(BaseModel):
    """SSP 2.0 traceability information"""
    element_id: str
    source_reference: Optional[str] = None
    requirements: List[str] = Field(default_factory=list)
    verification_status: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)