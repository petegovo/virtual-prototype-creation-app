# Virtual Prototype Creation App

A comprehensive web-based application for creating virtual prototypes using SystemC, Simulink, and Modelica IP through FMI 3.0 and SSP 2.0 standards.

## 🚀 Features

### Core Capabilities
- **FMI 3.0 Support**: Import, export, validate, and simulate Functional Mock-up Units (FMUs)
- **SSP 2.0 Integration**: System Structure and Parameterization for complex system modeling
- **Multi-Domain Modeling**: Support for SystemC, Simulink, and Modelica models
- **Co-Simulation**: Advanced simulation orchestration with real-time updates
- **Visual System Design**: Interactive 3D visualization and system composition
- **Project Management**: Comprehensive project lifecycle management

### Technical Features
- **Modern Web Architecture**: FastAPI backend with React/TypeScript frontend
- **Real-time Updates**: WebSocket support for live simulation monitoring
- **File Management**: Secure upload/download of FMU and SSP files
- **Validation Engine**: Comprehensive model validation and error reporting
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Database Integration**: Persistent storage with SQLite/SQLAlchemy

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Storage       │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│   (SQLite)      │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • FMI Parser    │    │ • Projects      │
│ • FMU Manager   │    │ • SSP Handler   │    │ • Models        │
│ • SSP Manager   │    │ • Simulator     │    │ • Simulations   │
│ • System Design │    │ • Validator     │    │ • Files         │
│ • Simulation    │    │ • File Manager  │    │                 │
│ • Projects      │    │ • WebSocket     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **FMPy**: Python library for FMI support
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server implementation

### Frontend
- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe JavaScript development
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching and state management
- **React Router**: Client-side routing
- **Three.js**: 3D graphics and visualization

### Development Tools
- **Vite**: Fast build tool and development server
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting

## 📦 Installation

### Quick Start with Podman (Recommended)

1. **Install Podman**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install -y podman
   
   # RHEL/CentOS/Fedora
   sudo dnf install -y podman
   
   # macOS
   brew install podman
   ```

2. **Run setup script**:
   ```bash
   ./setup-podman.sh
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Installation

#### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🚀 Usage

### Starting the Application

1. **Start the Backend** (Port 8000):
   ```bash
   cd backend
   python main.py
   ```

2. **Start the Frontend** (Port 12000+):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**:
   - Frontend: http://localhost:12000 (or next available port)
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### API Endpoints

#### FMI Operations
- `GET /api/fmi/list` - List all FMUs
- `POST /api/fmi/upload` - Upload FMU file
- `GET /api/fmi/{fmu_id}` - Get FMU details
- `POST /api/fmi/{fmu_id}/validate` - Validate FMU
- `POST /api/fmi/{fmu_id}/simulate` - Run simulation
- `GET /api/fmi/{fmu_id}/export` - Export FMU

#### SSP Operations
- `GET /api/ssp/list` - List all SSP packages
- `POST /api/ssp/upload` - Upload SSP file
- `GET /api/ssp/{ssp_id}` - Get SSP details
- `POST /api/ssp/{ssp_id}/validate` - Validate SSP

#### Project Management
- `GET /api/projects/list` - List all projects
- `POST /api/projects/create` - Create new project
- `GET /api/projects/{project_id}` - Get project details

#### Simulation
- `POST /api/simulation/start` - Start simulation
- `GET /api/simulation/status` - Get simulation status

## 🧪 Testing

### API Testing
```bash
python test_api.py
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📁 Project Structure

```
virtual-prototype-app/
├── backend/
│   ├── api/
│   │   ├── models/          # Pydantic models
│   │   └── routes/          # API route handlers
│   ├── fmi/                 # FMI 3.0 implementation
│   ├── ssp/                 # SSP 2.0 implementation
│   ├── simulation/          # Simulation engine
│   ├── storage/             # Database and file management
│   └── main.py              # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API services
│   │   └── types/           # TypeScript types
│   ├── public/              # Static assets
│   └── package.json         # Dependencies
├── uploads/                 # File storage
├── database/                # SQLite database
└── README.md
```

## 🔧 Configuration

### Environment Variables
```bash
# Backend
DATABASE_URL=sqlite:///./database/app.db
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=100MB

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

## 🌟 Key Features in Detail

### FMI 3.0 Support
- **Enhanced Co-simulation**: Advanced scheduling and event handling
- **Array Support**: Multi-dimensional array variables
- **Clock Support**: Discrete-time and continuous-time clocks
- **SystemC Integration**: Native support for SystemC models
- **Simulink Compatibility**: Direct import from Simulink models
- **Modelica Integration**: Seamless Modelica model integration

### SSP 2.0 Capabilities
- **System Structure**: Hierarchical system composition
- **Parameterization**: Advanced parameter management
- **Architectural Exchange**: System architecture sharing
- **FMI 3.0 Integration**: Full compatibility with FMI 3.0 models

### Virtual Prototype Features
- **3D Visualization**: Interactive 3D model representation
- **Real-time Simulation**: Live simulation with WebSocket updates
- **Model Composition**: Drag-and-drop system design
- **Parameter Tuning**: Interactive parameter adjustment
- **Results Analysis**: Comprehensive simulation results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the example projects in `/examples`

## 🔮 Roadmap

- [ ] WebSocket implementation for real-time updates
- [ ] 3D visualization with Three.js
- [ ] Advanced co-simulation orchestration
- [ ] Model marketplace integration
- [ ] Cloud deployment support
- [ ] Performance optimization
- [ ] Comprehensive testing suite
- [ ] Documentation and tutorials

---

**Virtual Prototype Creation App** - Bridging the gap between simulation and reality through FMI 3.0 and SSP 2.0 standards.