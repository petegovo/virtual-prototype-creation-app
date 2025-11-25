"""
Pydantic models for FMI 3.0 API endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime

class FMIVersion(str, Enum):
    """FMI version enumeration"""
    FMI_1_0 = "1.0"
    FMI_2_0 = "2.0"
    FMI_3_0 = "3.0"

class FMIType(str, Enum):
    """FMI interface type"""
    MODEL_EXCHANGE = "ModelExchange"
    CO_SIMULATION = "CoSimulation"
    SCHEDULED_EXECUTION = "ScheduledExecution"

class VariableType(str, Enum):
    """FMI variable types"""
    REAL = "Real"
    INTEGER = "Integer"
    BOOLEAN = "Boolean"
    STRING = "String"
    ENUMERATION = "Enumeration"
    BINARY = "Binary"
    CLOCK = "Clock"

class Causality(str, Enum):
    """Variable causality"""
    INPUT = "input"
    OUTPUT = "output"
    PARAMETER = "parameter"
    CALCULATED_PARAMETER = "calculatedParameter"
    LOCAL = "local"
    INDEPENDENT = "independent"

class Variability(str, Enum):
    """Variable variability"""
    CONSTANT = "constant"
    FIXED = "fixed"
    TUNABLE = "tunable"
    DISCRETE = "discrete"
    CONTINUOUS = "continuous"

class FMIVariable(BaseModel):
    """FMI variable definition"""
    name: str
    value_reference: int
    type: VariableType
    causality: Optional[Causality] = None
    variability: Optional[Variability] = None
    initial: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    display_unit: Optional[str] = None
    min_value: Optional[Union[float, int]] = None
    max_value: Optional[Union[float, int]] = None
    nominal: Optional[float] = None
    start_value: Optional[Union[float, int, bool, str]] = None
    dimensions: Optional[List[int]] = None  # FMI 3.0 arrays

class FMUInfo(BaseModel):
    """FMU information model"""
    guid: str
    fmi_version: FMIVersion
    model_name: str
    description: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = None
    copyright: Optional[str] = None
    license: Optional[str] = None
    generation_tool: Optional[str] = None
    generation_date_and_time: Optional[datetime] = None
    variable_naming_convention: Optional[str] = None
    number_of_event_indicators: Optional[int] = None
    supports_co_simulation: bool = False
    supports_model_exchange: bool = False
    supports_scheduled_execution: bool = False  # FMI 3.0
    
class FMUVariables(BaseModel):
    """FMU variables collection"""
    variables: List[FMIVariable]
    inputs: List[FMIVariable] = Field(default_factory=list)
    outputs: List[FMIVariable] = Field(default_factory=list)
    parameters: List[FMIVariable] = Field(default_factory=list)

class FMUUploadResponse(BaseModel):
    """Response model for FMU upload"""
    fmu_id: str
    filename: str
    file_size: int
    upload_time: datetime
    info: FMUInfo
    variables: FMUVariables
    validation_status: str
    validation_messages: List[str] = Field(default_factory=list)

class FMUListResponse(BaseModel):
    """Response model for FMU list"""
    fmus: List[FMUUploadResponse]
    total_count: int

class FMUExportRequest(BaseModel):
    """Request model for FMU export"""
    fmu_id: str
    export_format: FMIVersion = FMIVersion.FMI_3_0
    include_source: bool = False
    target_platform: Optional[str] = None

class FMUValidationResult(BaseModel):
    """FMU validation result"""
    is_valid: bool
    fmi_version: FMIVersion
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    info_messages: List[str] = Field(default_factory=list)

class FMUSimulationConfig(BaseModel):
    """FMU simulation configuration"""
    start_time: float = 0.0
    stop_time: float = 1.0
    step_size: Optional[float] = None
    tolerance: Optional[float] = 1e-6
    solver: Optional[str] = None
    output_interval: Optional[float] = None
    log_level: int = 2  # 0=all, 1=error, 2=warning, 3=info, 4=verbose, 5=debug

class FMUParameterSet(BaseModel):
    """FMU parameter configuration"""
    parameters: Dict[str, Union[float, int, bool, str]]
    description: Optional[str] = None

class FMUConnection(BaseModel):
    """Connection between FMU variables"""
    source_fmu: str
    source_variable: str
    target_fmu: str
    target_variable: str
    connection_type: str = "direct"  # direct, algebraic_loop, etc.