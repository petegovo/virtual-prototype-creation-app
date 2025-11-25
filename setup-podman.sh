#!/bin/bash

# Virtual Prototype Creation App - Podman Setup Script
# This script sets up the application using Podman instead of Docker

set -e

echo "🚀 Virtual Prototype Creation App - Podman Setup"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for rootless Podman setup"
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check for Podman
if ! command_exists podman; then
    print_error "Podman is not installed. Please install Podman first:"
    echo "  Ubuntu/Debian: sudo apt-get install -y podman"
    echo "  RHEL/CentOS/Fedora: sudo dnf install -y podman"
    echo "  macOS: brew install podman"
    exit 1
fi

print_success "Podman found: $(podman --version)"

# Check for Python
if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

print_success "Python found: $(python3 --version)"

# Check for pip
if ! command_exists pip3; then
    print_error "pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install podman-compose if not present
if ! command_exists podman-compose; then
    print_status "Installing podman-compose..."
    pip3 install --user podman-compose
    
    # Add to PATH if needed
    if ! command_exists podman-compose; then
        export PATH="$HOME/.local/bin:$PATH"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    fi
fi

print_success "podman-compose found: $(podman-compose --version)"

# Configure Podman for rootless operation
print_status "Configuring Podman for rootless operation..."

# Check if user namespaces are configured
if ! grep -q "^$(whoami):" /etc/subuid 2>/dev/null; then
    print_warning "User namespaces not configured. You may need to run:"
    echo "  sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $(whoami)"
    echo "  podman system migrate"
fi

# Initialize Podman if needed
if [ ! -d "$HOME/.local/share/containers" ]; then
    print_status "Initializing Podman..."
    podman system migrate
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p uploads database logs

# Set up environment
print_status "Setting up environment..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cat > .env << EOF
# Database Configuration
DATABASE_URL=sqlite:///./database/app.db

# Upload Configuration
UPLOAD_DIR=./uploads

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000

# Development Configuration
DEBUG=true
LOG_LEVEL=INFO
EOF
    print_success "Created .env file"
fi

# Build and start services
print_status "Building and starting services with Podman..."

# Check if podman-compose.yml exists, otherwise use docker-compose.yml
COMPOSE_FILE="podman-compose.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
    COMPOSE_FILE="docker-compose.yml"
    print_warning "Using docker-compose.yml (consider renaming to podman-compose.yml)"
fi

# Build images
print_status "Building container images..."
podman-compose -f "$COMPOSE_FILE" build

# Start services
print_status "Starting services..."
podman-compose -f "$COMPOSE_FILE" up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Check service health
print_status "Checking service health..."

# Check backend
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    print_success "Backend is healthy"
else
    print_warning "Backend health check failed"
fi

# Check frontend
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    print_success "Frontend is healthy"
else
    print_warning "Frontend health check failed"
fi

# Display status
print_status "Displaying container status..."
podman ps

echo ""
print_success "Setup completed successfully!"
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "   View logs: podman-compose -f $COMPOSE_FILE logs"
echo "   Stop services: podman-compose -f $COMPOSE_FILE down"
echo "   Restart services: podman-compose -f $COMPOSE_FILE restart"
echo "   View containers: podman ps"
echo ""
echo "🔧 Troubleshooting:"
echo "   Check logs: podman logs <container_name>"
echo "   System info: podman system info"
echo "   Reset if needed: podman system migrate"
echo ""
print_success "Happy prototyping! 🚀"