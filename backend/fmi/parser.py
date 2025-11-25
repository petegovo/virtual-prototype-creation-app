"""
FMI 3.0 Parser using FMPy library
Handles parsing of FMU files and extraction of model information
"""

import logging
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import tempfile
import shutil

try:
    import fmpy
    from fmpy import read_model_description
    from fmpy.util import download_test_file
except ImportError:
    fmpy = None
    logging.warning("FMPy not available. FMI functionality will be limited.")

from api.models.fmi_models import (
    FMUInfo, FMIVariable, FMUVariables, FMIVersion, FMIType,
    VariableType, Causality, Variability
)

logger = logging.getLogger(__name__)

class FMIParser:
    """Parser for FMI files using FMPy"""
    
    def __init__(self):
        if not fmpy:
            raise ImportError("FMPy library is required for FMI parsing")
    
    async def parse_fmu(self, fmu_path: Path) -> Dict[str, Any]:
        """
        Parse an FMU file and extract all relevant information
        
        Args:
            fmu_path: Path to the FMU file
            
        Returns:
            Dictionary containing FMU information and variables
        """
        try:
            logger.info(f"Parsing FMU: {fmu_path}")
            
            # Read model description using FMPy
            model_description = read_model_description(str(fmu_path))
            
            # Extract basic FMU information
            fmu_info = self._extract_fmu_info(model_description)
            
            # Extract variables
            variables = self._extract_variables(model_description)
            
            # Categorize variables
            categorized_vars = self._categorize_variables(variables)
            
            return {
                "info": fmu_info,
                "variables": categorized_vars,
                "model_description": model_description
            }
            
        except Exception as e:
            logger.error(f"Error parsing FMU {fmu_path}: {str(e)}")
            raise
    
    def _extract_fmu_info(self, model_description: Dict[str, Any]) -> FMUInfo:
        """Extract basic FMU information from model description"""
        
        # Determine FMI version
        fmi_version = FMIVersion.FMI_2_0  # Default
        if 'fmiVersion' in model_description:
            version_str = model_description['fmiVersion']
            if version_str.startswith('3.'):
                fmi_version = FMIVersion.FMI_3_0
            elif version_str.startswith('2.'):
                fmi_version = FMIVersion.FMI_2_0
            elif version_str.startswith('1.'):
                fmi_version = FMIVersion.FMI_1_0
        
        # Parse generation date
        generation_date = None
        if 'generationDateAndTime' in model_description:
            try:
                generation_date = datetime.fromisoformat(
                    model_description['generationDateAndTime'].replace('Z', '+00:00')
                )
            except:
                pass
        
        # Check interface types
        supports_co_simulation = 'CoSimulation' in model_description
        supports_model_exchange = 'ModelExchange' in model_description
        supports_scheduled_execution = 'ScheduledExecution' in model_description  # FMI 3.0
        
        return FMUInfo(
            guid=model_description.get('guid', ''),
            fmi_version=fmi_version,
            model_name=model_description.get('modelName', ''),
            description=model_description.get('description'),
            author=model_description.get('author'),
            version=model_description.get('version'),
            copyright=model_description.get('copyright'),
            license=model_description.get('license'),
            generation_tool=model_description.get('generationTool'),
            generation_date_and_time=generation_date,
            variable_naming_convention=model_description.get('variableNamingConvention'),
            number_of_event_indicators=model_description.get('numberOfEventIndicators'),
            supports_co_simulation=supports_co_simulation,
            supports_model_exchange=supports_model_exchange,
            supports_scheduled_execution=supports_scheduled_execution
        )
    
    def _extract_variables(self, model_description: Dict[str, Any]) -> List[FMIVariable]:
        """Extract variables from model description"""
        variables = []
        
        model_variables = model_description.get('modelVariables', [])
        
        for var_data in model_variables:
            try:
                variable = self._parse_variable(var_data)
                if variable:
                    variables.append(variable)
            except Exception as e:
                logger.warning(f"Error parsing variable {var_data.get('name', 'unknown')}: {str(e)}")
                continue
        
        return variables
    
    def _parse_variable(self, var_data: Dict[str, Any]) -> Optional[FMIVariable]:
        """Parse a single variable from model description"""
        
        # Determine variable type
        var_type = VariableType.REAL  # Default
        type_info = None
        
        for type_name in ['Real', 'Integer', 'Boolean', 'String', 'Enumeration', 'Binary', 'Clock']:
            if type_name in var_data:
                var_type = VariableType(type_name.upper() if type_name.upper() in VariableType.__members__ else 'REAL')
                type_info = var_data[type_name]
                break
        
        # Parse causality
        causality = None
        if 'causality' in var_data:
            try:
                causality = Causality(var_data['causality'])
            except ValueError:
                pass
        
        # Parse variability
        variability = None
        if 'variability' in var_data:
            try:
                variability = Variability(var_data['variability'])
            except ValueError:
                pass
        
        # Extract start value
        start_value = None
        if type_info and 'start' in type_info:
            start_value = type_info['start']
        
        # Extract min/max values
        min_value = None
        max_value = None
        if type_info:
            min_value = type_info.get('min')
            max_value = type_info.get('max')
        
        # Extract dimensions for FMI 3.0 arrays
        dimensions = None
        if 'dimensions' in var_data:
            dimensions = var_data['dimensions']
        
        return FMIVariable(
            name=var_data.get('name', ''),
            value_reference=var_data.get('valueReference', 0),
            type=var_type,
            causality=causality,
            variability=variability,
            initial=var_data.get('initial'),
            description=var_data.get('description'),
            unit=type_info.get('unit') if type_info else None,
            display_unit=type_info.get('displayUnit') if type_info else None,
            min_value=min_value,
            max_value=max_value,
            nominal=type_info.get('nominal') if type_info else None,
            start_value=start_value,
            dimensions=dimensions
        )
    
    def _categorize_variables(self, variables: List[FMIVariable]) -> FMUVariables:
        """Categorize variables by causality"""
        inputs = []
        outputs = []
        parameters = []
        
        for var in variables:
            if var.causality == Causality.INPUT:
                inputs.append(var)
            elif var.causality == Causality.OUTPUT:
                outputs.append(var)
            elif var.causality in [Causality.PARAMETER, Causality.CALCULATED_PARAMETER]:
                parameters.append(var)
        
        return FMUVariables(
            variables=variables,
            inputs=inputs,
            outputs=outputs,
            parameters=parameters
        )
    
    async def extract_fmu_resources(self, fmu_path: Path) -> Dict[str, bytes]:
        """
        Extract additional resources from FMU (documentation, sources, etc.)
        
        Args:
            fmu_path: Path to the FMU file
            
        Returns:
            Dictionary mapping resource paths to their content
        """
        resources = {}
        
        try:
            with zipfile.ZipFile(fmu_path, 'r') as zip_file:
                for file_info in zip_file.filelist:
                    # Skip the main model description
                    if file_info.filename == 'modelDescription.xml':
                        continue
                    
                    # Extract interesting files
                    if (file_info.filename.startswith('documentation/') or
                        file_info.filename.startswith('sources/') or
                        file_info.filename.endswith('.md') or
                        file_info.filename.endswith('.txt')):
                        
                        try:
                            content = zip_file.read(file_info.filename)
                            resources[file_info.filename] = content
                        except Exception as e:
                            logger.warning(f"Could not extract {file_info.filename}: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error extracting resources from {fmu_path}: {str(e)}")
        
        return resources
    
    def get_supported_platforms(self, fmu_path: Path) -> List[str]:
        """
        Get list of supported platforms from FMU
        
        Args:
            fmu_path: Path to the FMU file
            
        Returns:
            List of supported platform identifiers
        """
        platforms = []
        
        try:
            with zipfile.ZipFile(fmu_path, 'r') as zip_file:
                for file_info in zip_file.filelist:
                    if file_info.filename.startswith('binaries/'):
                        # Extract platform from path like binaries/win64/model.dll
                        path_parts = file_info.filename.split('/')
                        if len(path_parts) >= 2:
                            platform = path_parts[1]
                            if platform not in platforms:
                                platforms.append(platform)
        
        except Exception as e:
            logger.error(f"Error getting platforms from {fmu_path}: {str(e)}")
        
        return platforms