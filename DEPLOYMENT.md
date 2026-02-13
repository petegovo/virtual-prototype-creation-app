# Deployment Guide

This guide covers various deployment options for the Virtual Prototype Creation App.

## Table of Contents

1. [Local Development](#local-development)
2. [Podman Deployment](#podman-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)
5. [Monitoring and Logging](#monitoring-and-logging)

## Local Development

### Prerequisites
- Python 3.8+ 
- Node.js 18+
- Git

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/virtual-prototype-creation-app.git
   cd virtual-prototype-creation-app
   ```

2. **Backend setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend setup**:
   ```bash
   cd frontend
   npm install
   ```

4. **Start development servers**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   python main.py

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

5. **Access the application**:
   - Frontend: http://localhost:12000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Podman Deployment

### Quick Start with Podman Compose

1. **Install Podman and podman-compose**:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y podman
   pip install podman-compose
   
   # On RHEL/CentOS/Fedora
   sudo dnf install -y podman
   pip install podman-compose
   ```

2. **Clone and start**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/virtual-prototype-creation-app.git
   cd virtual-prototype-creation-app
   podman-compose up -d
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Production Podman Compose

For production with PostgreSQL and Redis:

```bash
# Start with production profile
podman-compose --profile production up -d

# Or create a production override file
cp podman-compose.yml podman-compose.prod.yml
# Edit podman-compose.prod.yml for production settings
podman-compose -f podman-compose.yml -f podman-compose.prod.yml up -d
```

### Individual Container Deployment

1. **Build images**:
   ```bash
   # Backend
   podman build -t virtual-prototype-backend ./backend

   # Frontend
   podman build -t virtual-prototype-frontend ./frontend
   ```

2. **Run containers**:
   ```bash
   # Create network
   podman network create virtual-prototype-network

   # Run backend
   podman run -d \
     --name backend \
     --network virtual-prototype-network \
     -p 8000:8000 \
     -v $(pwd)/uploads:/app/uploads:Z \
     -v $(pwd)/database:/app/database:Z \
     virtual-prototype-backend

   # Run frontend
   podman run -d \
     --name frontend \
     --network virtual-prototype-network \
     -p 3000:3000 \
     virtual-prototype-frontend
   ```

## Cloud Deployment

### AWS Deployment

#### Option 1: AWS ECS with Fargate

1. **Create ECS cluster**:
   ```bash
   aws ecs create-cluster --cluster-name virtual-prototype-cluster
   ```

2. **Create task definition** (`ecs-task-definition.json`):
   ```json
   {
     "family": "virtual-prototype",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "1024",
     "memory": "2048",
     "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "backend",
         "image": "YOUR_DOCKER_HUB/virtual-prototype-backend:latest",
         "portMappings": [{"containerPort": 8000}],
         "environment": [
           {"name": "DATABASE_URL", "value": "postgresql://..."}
         ]
       },
       {
         "name": "frontend",
         "image": "YOUR_DOCKER_HUB/virtual-prototype-frontend:latest",
         "portMappings": [{"containerPort": 3000}]
       }
     ]
   }
   ```

3. **Deploy service**:
   ```bash
   aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
   aws ecs create-service \
     --cluster virtual-prototype-cluster \
     --service-name virtual-prototype-service \
     --task-definition virtual-prototype \
     --desired-count 2 \
     --launch-type FARGATE
   ```

#### Option 2: AWS App Runner

1. **Create apprunner.yaml**:
   ```yaml
   version: 1.0
   runtime: docker
   build:
     commands:
       build:
         - echo "Building application"
   run:
     runtime-version: latest
     command: python main.py
     network:
       port: 8000
       env: PORT
   ```

2. **Deploy with App Runner**:
   ```bash
   aws apprunner create-service \
     --service-name virtual-prototype-backend \
     --source-configuration '{
       "ImageRepository": {
         "ImageIdentifier": "YOUR_DOCKER_HUB/virtual-prototype-backend:latest",
         "ImageConfiguration": {
           "Port": "8000"
         },
         "ImageRepositoryType": "ECR_PUBLIC"
       },
       "AutoDeploymentsEnabled": true
     }'
   ```

### Google Cloud Platform

#### Cloud Run Deployment

1. **Deploy backend**:
   ```bash
   gcloud run deploy virtual-prototype-backend \
     --image YOUR_DOCKER_HUB/virtual-prototype-backend:latest \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8000
   ```

2. **Deploy frontend**:
   ```bash
   gcloud run deploy virtual-prototype-frontend \
     --image YOUR_DOCKER_HUB/virtual-prototype-frontend:latest \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 3000
   ```

### Azure Container Instances

1. **Create resource group**:
   ```bash
   az group create --name virtual-prototype-rg --location eastus
   ```

2. **Deploy containers**:
   ```bash
   az container create \
     --resource-group virtual-prototype-rg \
     --name virtual-prototype-app \
     --image YOUR_DOCKER_HUB/virtual-prototype-backend:latest \
     --dns-name-label virtual-prototype-backend \
     --ports 8000
   ```

### Kubernetes Deployment

1. **Create namespace**:
   ```bash
   kubectl create namespace virtual-prototype
   ```

2. **Apply Kubernetes manifests** (`k8s/`):
   ```yaml
   # deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: virtual-prototype-backend
     namespace: virtual-prototype
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: virtual-prototype-backend
     template:
       metadata:
         labels:
           app: virtual-prototype-backend
       spec:
         containers:
         - name: backend
           image: YOUR_DOCKER_HUB/virtual-prototype-backend:latest
           ports:
           - containerPort: 8000
           env:
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: database-secret
                 key: url
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: virtual-prototype-backend-service
     namespace: virtual-prototype
   spec:
     selector:
       app: virtual-prototype-backend
     ports:
     - port: 80
       targetPort: 8000
     type: LoadBalancer
   ```

3. **Deploy**:
   ```bash
   kubectl apply -f k8s/
   ```

## Production Considerations

### Environment Variables

Create a `.env` file for production:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# File Storage
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=100MB

# Redis (if using)
REDIS_URL=redis://redis:6379/0

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Database Setup

#### PostgreSQL (Recommended for Production)

1. **Create database**:
   ```sql
   CREATE DATABASE virtual_prototype;
   CREATE USER vpuser WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE virtual_prototype TO vpuser;
   ```

2. **Update connection string**:
   ```env
   DATABASE_URL=postgresql://vpuser:secure_password@localhost:5432/virtual_prototype
   ```

#### Database Migrations

```bash
# Run migrations (if using Alembic)
alembic upgrade head

# Or initialize database
python -c "from storage.database import init_db; init_db()"
```

### SSL/TLS Configuration

#### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/virtual-prototype`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://localhost:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### Performance Optimization

#### Backend Optimization

1. **Use Gunicorn with multiple workers**:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. **Add caching**:
   ```python
   # Add Redis caching
   import redis
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.redis import RedisBackend

   redis_client = redis.Redis(host="redis", port=6379, db=0)
   FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
   ```

#### Frontend Optimization

1. **Build optimization**:
   ```bash
   npm run build
   # Serve static files with nginx or CDN
   ```

2. **Enable compression in nginx**:
   ```nginx
   gzip on;
   gzip_vary on;
   gzip_min_length 1024;
   gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
   ```

### Security Hardening

1. **Update Dockerfile for security**:
   ```dockerfile
   # Use non-root user
   RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
   USER nextjs

   # Remove unnecessary packages
   RUN apt-get remove --purge -y build-essential && apt-get autoremove -y
   ```

2. **Set security headers**:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   from fastapi.middleware.trustedhost import TrustedHostMiddleware

   app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "DELETE"],
       allow_headers=["*"],
   )
   ```

## Monitoring and Logging

### Application Monitoring

1. **Add health checks**:
   ```python
   @app.get("/health")
   async def health_check():
       return {
           "status": "healthy",
           "timestamp": datetime.utcnow(),
           "version": "1.0.0"
       }
   ```

2. **Prometheus metrics**:
   ```bash
   pip install prometheus-fastapi-instrumentator
   ```

   ```python
   from prometheus_fastapi_instrumentator import Instrumentator

   Instrumentator().instrument(app).expose(app)
   ```

### Logging Configuration

```python
import logging
from pythonjsonlogger import jsonlogger

# Configure structured logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### Error Tracking

1. **Sentry integration**:
   ```bash
   pip install sentry-sdk[fastapi]
   ```

   ```python
   import sentry_sdk
   from sentry_sdk.integrations.fastapi import FastApiIntegration

   sentry_sdk.init(
       dsn="YOUR_SENTRY_DSN",
       integrations=[FastApiIntegration()],
       traces_sample_rate=1.0,
   )
   ```

### Backup Strategy

1. **Database backups**:
   ```bash
   # PostgreSQL backup
   pg_dump -h localhost -U vpuser virtual_prototype > backup_$(date +%Y%m%d_%H%M%S).sql

   # Automated backup script
   #!/bin/bash
   BACKUP_DIR="/backups"
   DATE=$(date +%Y%m%d_%H%M%S)
   pg_dump -h localhost -U vpuser virtual_prototype | gzip > $BACKUP_DIR/backup_$DATE.sql.gz
   find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
   ```

2. **File storage backups**:
   ```bash
   # Sync uploads to S3
   aws s3 sync ./uploads s3://your-backup-bucket/uploads/
   ```

## Troubleshooting

### Common Issues

1. **Port conflicts**:
   ```bash
   # Check what's using the port
   lsof -i :8000
   # Kill the process
   kill -9 PID
   ```

2. **Database connection issues**:
   ```bash
   # Test database connection
   psql -h localhost -U vpuser -d virtual_prototype -c "SELECT 1;"
   ```

3. **Podman issues**:
   ```bash
   # Check container logs
   podman logs container_name
   # Restart containers
   podman-compose restart
   
   # Check rootless configuration
   podman system info
   
   # Reset user namespace if needed
   podman system migrate
   ```

4. **Memory issues**:
   ```bash
   # Monitor memory usage
   podman stats
   # Increase container memory limits in compose file
   ```

### Performance Monitoring

1. **Monitor application metrics**:
   - Response times
   - Error rates
   - Database query performance
   - Memory and CPU usage

2. **Set up alerts**:
   - High error rates
   - Slow response times
   - Database connection issues
   - Disk space usage

---

This deployment guide provides comprehensive instructions for deploying the Virtual Prototype Creation App in various environments. Choose the deployment method that best fits your infrastructure and requirements.