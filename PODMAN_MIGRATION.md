# 🔄 Podman Migration Guide

This document explains the migration from Docker to Podman for the Virtual Prototype Creation App, including the benefits, changes made, and how to use the new Podman-based setup.

## 🎯 Why Podman?

### Key Benefits

1. **Rootless Containers**: Enhanced security by running containers without root privileges
2. **Daemonless Architecture**: No background daemon required, reducing attack surface
3. **OCI Compliance**: Full compatibility with Docker images and containers
4. **Systemd Integration**: Native integration with systemd for better service management
5. **Pod Support**: Kubernetes-style pod management for multi-container applications
6. **Resource Efficiency**: Lower memory footprint and better resource utilization

### Security Advantages

- **No Root Daemon**: Eliminates the security risk of a privileged daemon
- **User Namespaces**: Containers run in isolated user namespaces
- **SELinux Integration**: Better integration with SELinux security policies
- **Reduced Attack Surface**: Fewer privileged processes running on the host

## 🔧 Changes Made

### 1. Container Orchestration

**Before (Docker Compose)**:
```yaml
version: '3.8'
services:
  backend:
    volumes:
      - ./uploads:/app/uploads
```

**After (Podman Compose)**:
```yaml
version: '3.8'
services:
  backend:
    volumes:
      - ./uploads:/app/uploads:Z  # SELinux label for shared volumes
    security_opt:
      - label=disable  # Disable SELinux confinement if needed
```

### 2. CI/CD Pipeline

**Before (GitHub Actions with Docker)**:
```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
```

**After (GitHub Actions with Podman)**:
```yaml
- name: Install Podman
  run: sudo apt-get install -y podman

- name: Build and push with Podman
  run: |
    podman build -t image:tag .
    podman push image:tag
```

### 3. Development Scripts

**Before**:
```bash
docker-compose up -d
docker logs container_name
```

**After**:
```bash
podman-compose up -d
podman logs container_name
```

## 📋 Migration Steps

### 1. Install Podman

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y podman
```

#### RHEL/CentOS/Fedora
```bash
sudo dnf install -y podman
```

#### macOS
```bash
brew install podman
```

### 2. Install podman-compose
```bash
pip install podman-compose
```

### 3. Configure Rootless Operation

```bash
# Configure user namespaces (if not already done)
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER

# Initialize Podman
podman system migrate

# Configure registries
mkdir -p ~/.config/containers
cat > ~/.config/containers/registries.conf << EOF
[registries.search]
registries = ['docker.io', 'quay.io']
EOF
```

### 4. Update Your Workflow

Replace Docker commands with Podman equivalents:

| Docker Command | Podman Equivalent |
|----------------|-------------------|
| `docker build` | `podman build` |
| `docker run` | `podman run` |
| `docker ps` | `podman ps` |
| `docker logs` | `podman logs` |
| `docker-compose up` | `podman-compose up` |
| `docker-compose down` | `podman-compose down` |

## 🚀 Quick Start

### Using the Setup Script
```bash
# Clone the repository
git clone https://github.com/petegovo/virtual-prototype-creation-app.git
cd virtual-prototype-creation-app

# Run the Podman setup script
./setup-podman.sh
```

### Manual Setup
```bash
# Build and start services
podman-compose up -d --build

# Check status
podman ps

# View logs
podman-compose logs

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 🔍 Key Differences from Docker

### Volume Mounting
Podman requires SELinux labels for shared volumes:
```bash
# Docker
-v /host/path:/container/path

# Podman
-v /host/path:/container/path:Z
```

### Networking
Podman uses different default networks:
```bash
# List networks
podman network ls

# Create custom network
podman network create mynetwork
```

### Registry Configuration
Podman uses `registries.conf` for registry configuration:
```bash
# Location: ~/.config/containers/registries.conf
[registries.search]
registries = ['docker.io', 'quay.io']
```

## 🛠️ Development Workflow

### Daily Development
```bash
# Start development environment
podman-compose up -d

# View logs
podman-compose logs -f

# Restart a service
podman-compose restart backend

# Stop everything
podman-compose down
```

### Building Images
```bash
# Build backend image
podman build -t virtual-prototype-backend ./backend

# Build frontend image
podman build -t virtual-prototype-frontend ./frontend

# List images
podman images
```

### Debugging
```bash
# Execute commands in running container
podman exec -it container_name bash

# Check container details
podman inspect container_name

# Monitor resource usage
podman stats
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Permission Denied
```bash
# Check user namespaces
cat /etc/subuid | grep $USER
cat /etc/subgid | grep $USER

# If missing, configure:
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
```

#### 2. SELinux Issues
```bash
# Check SELinux status
sestatus

# If SELinux is enforcing and causing issues:
# Option 1: Use :Z label for volumes
-v /host/path:/container/path:Z

# Option 2: Disable SELinux for container (less secure)
--security-opt label=disable
```

#### 3. Registry Issues
```bash
# Check registry configuration
podman info

# Test registry access
podman pull docker.io/library/hello-world
```

#### 4. Network Issues
```bash
# Check networks
podman network ls

# Inspect network
podman network inspect network_name

# Recreate network if needed
podman network rm network_name
podman network create network_name
```

### Reset Podman
If you encounter persistent issues:
```bash
# Stop all containers
podman stop --all

# Remove all containers
podman rm --all

# Remove all images
podman rmi --all

# Reset system
podman system reset
podman system migrate
```

## 📊 Performance Comparison

| Metric | Docker | Podman |
|--------|--------|--------|
| Memory Usage | Higher (daemon) | Lower (daemonless) |
| Startup Time | Slower | Faster |
| Security | Root daemon | Rootless |
| Resource Overhead | Higher | Lower |
| Systemd Integration | Limited | Native |

## 🔐 Security Best Practices

### 1. Use Rootless Mode
Always run Podman in rootless mode for enhanced security:
```bash
# Check if running rootless
podman system info | grep rootless
```

### 2. Configure SELinux
Use proper SELinux labels for volumes:
```bash
# For shared volumes
-v /host/path:/container/path:Z

# For private volumes
-v /host/path:/container/path:z
```

### 3. Limit Resources
Set resource limits in compose files:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

### 4. Use Non-root Users
Ensure Dockerfiles use non-root users:
```dockerfile
RUN adduser -D -s /bin/sh appuser
USER appuser
```

## 📚 Additional Resources

- [Podman Official Documentation](https://docs.podman.io/)
- [Podman vs Docker Comparison](https://docs.podman.io/en/latest/markdown/podman.1.html)
- [Rootless Containers Guide](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md)
- [podman-compose Documentation](https://github.com/containers/podman-compose)

## 🎉 Benefits Realized

After migrating to Podman, you'll experience:

- ✅ **Enhanced Security**: Rootless containers reduce attack surface
- ✅ **Better Performance**: Lower memory usage and faster startup
- ✅ **Improved Integration**: Native systemd support
- ✅ **Simplified Management**: No daemon to manage
- ✅ **Full Compatibility**: Works with existing Docker images
- ✅ **Enterprise Ready**: Better suited for production environments

---

*This migration maintains full compatibility with existing Docker workflows while providing enhanced security and performance benefits.*