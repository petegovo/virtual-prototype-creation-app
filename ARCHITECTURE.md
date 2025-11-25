# Virtual Prototype Creation App Architecture

## Overview
A web-based virtual prototype creation application that enables reuse of SystemC, Simulink, and Modelica IP via FMI 3.0 and SSP 2.0 import/export capabilities.

## System Architecture

### Technology Stack
- **Backend**: Python 3.11+ with FastAPI
- **FMI/SSP Processing**: FMPy library for FMI 3.0 support
- **Frontend**: React 18+ with TypeScript
- **Visualization**: Three.js for 3D visualization, D3.js for charts/graphs
- **File Storage**: Local filesystem with metadata in SQLite
- **API**: RESTful API with WebSocket for real-time simulation updates

### Core Components

#### 1. Backend Services (`/backend`)
- **API Layer** (`api/`): FastAPI routes for FMU/SSP management
- **FMI Handler** (`fmi/`): FMI 3.0 import/export using FMPy
- **SSP Handler** (`ssp/`): SSP 2.0 system structure management
- **Simulation Engine** (`simulation/`): Co-simulation orchestration
- **File Manager** (`storage/`): FMU/SSP file handling and metadata
- **WebSocket Handler** (`websocket/`): Real-time simulation updates

#### 2. Frontend Application (`/frontend`)
- **Model Manager**: Import/export FMU and SSP files
- **System Designer**: Visual system composition and connection
- **Parameter Editor**: Model parameterization interface
- **Simulation Controller**: Start/stop/configure simulations
- **Visualization Engine**: 3D model visualization and results plotting
- **Project Manager**: Save/load virtual prototype projects

#### 3. Core Features

##### FMI 3.0 Support
- Import FMUs from SystemC, Simulink, and Modelica tools
- Support for all FMI 3.0 data types (arrays, clocks, binary)
- Co-simulation and Model Exchange modes
- Scheduled execution support
- Event handling and intermediate updates

##### SSP 2.0 Support
- System structure definition and exchange
- Parameter sets and configurations
- Architectural specifications
- Traceability and metadata management
- FMI 3.0 integration

##### Virtual Prototyping Capabilities
- Multi-domain model integration
- Real-time co-simulation
- Interactive parameter tuning
- Results visualization and analysis
- System-level validation

## Data Flow

1. **Model Import**: Users upload FMU/SSP files
2. **Model Analysis**: Backend extracts metadata and interfaces
3. **System Composition**: Frontend provides visual system design
4. **Parameter Configuration**: Users set model parameters
5. **Simulation Execution**: Backend orchestrates co-simulation
6. **Results Visualization**: Real-time updates via WebSocket
7. **Export**: Generate SSP packages for system exchange

## File Structure
```
/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   ├── models/
│   │   └── middleware/
│   ├── fmi/
│   │   ├── parser.py
│   │   ├── simulator.py
│   │   └── validator.py
│   ├── ssp/
│   │   ├── parser.py
│   │   ├── generator.py
│   │   └── validator.py
│   ├── simulation/
│   │   ├── engine.py
│   │   ├── scheduler.py
│   │   └── coordinator.py
│   ├── storage/
│   │   ├── file_manager.py
│   │   ├── metadata.py
│   │   └── database.py
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── types/
│   │   └── utils/
│   ├── public/
│   └── package.json
├── shared/
│   ├── schemas/
│   └── types/
└── docs/
```

## Key Design Principles

1. **Modularity**: Separate concerns for FMI, SSP, and simulation
2. **Extensibility**: Plugin architecture for new model types
3. **Performance**: Efficient handling of large FMU files
4. **Usability**: Intuitive web interface for complex operations
5. **Standards Compliance**: Full FMI 3.0 and SSP 2.0 conformance
6. **Interoperability**: Support for multiple tool ecosystems

## Security Considerations

- File upload validation and sandboxing
- FMU binary execution in isolated environment
- Input sanitization for all user data
- CORS configuration for web API access
- Secure file storage and access controls