# FedHR5.0 Deployment Guide

> Production deployment instructions for FedHR5.0 in Industry 5.0 environments

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Deployment Options](#deployment-options)
3. [Quick Start](#quick-start)
4. [Production Deployment](#production-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Bare Metal Installation](#bare-metal-installation)
8. [Configuration](#configuration)
9. [Security Hardening](#security-hardening)
10. [Monitoring & Observability](#monitoring--observability)
11. [Troubleshooting](#troubleshooting)
12. [Maintenance](#maintenance)

## Prerequisites

### System Requirements

#### Minimum Requirements

| Component | Specification | Purpose |
|-----------|---------------|---------|
| **Edge Device** | | |
| CPU | 2 cores (ARM/x86) | Local training |
| RAM | 4 GB | Model storage |
| Storage | 50 GB SSD | Data caching |
| Network | 10 Mbps | Model updates |
| **Fog Server** | | |
| CPU | 8 cores | Aggregation |
| RAM | 32 GB | Multiple models |
| Storage | 500 GB SSD | Logs & models |
| Network | 100 Mbps | Client handling |
| **Cloud Server** | | |
| CPU | 16 cores | Global coordination |
| RAM | 64 GB | Concurrent training |
| Storage | 2 TB SSD | Historical data |
| Network | 1 Gbps | High throughput |

#### Recommended Production Specifications

```yaml
# production-requirements.yaml
edge_device:
  cpu: 4 cores
  ram: 8 GB
  storage: 100 GB NVMe
  network: 50 Mbps
  gpu: Optional (Jetson Nano)

fog_server:
  cpu: 16 cores
  ram: 64 GB
  storage: 1 TB NVMe
  network: 1 Gbps
  gpu: NVIDIA T4 (optional)

cloud_server:
  cpu: 32 cores
  ram: 128 GB
  storage: 4 TB NVMe RAID
  network: 10 Gbps
  gpu: NVIDIA A100 (recommended)
```

### Software Dependencies

```bash
# Operating System
- Ubuntu 20.04 LTS or later
- RHEL 8+ (enterprise)
- Debian 11+

# Runtime
- Python 3.8+
- Docker 20.10+
- Kubernetes 1.21+ (for K8s deployment)

# Databases
- PostgreSQL 13+
- Redis 6+
- TimescaleDB 2+ (optional)

# Blockchain (if using)
- Hyperledger Fabric 2.4+
- Go 1.16+
```

## Deployment Options

### Decision Matrix

| Deployment Type | Best For | Pros | Cons |
|----------------|----------|------|------|
| **Docker Compose** | Development, Small deployments | Easy setup, Portable | Limited scaling |
| **Kubernetes** | Production, Multi-site | Scalable, Resilient | Complex setup |
| **Bare Metal** | High performance, Security | Full control, Performance | Manual management |
| **Hybrid Cloud** | Enterprise, Compliance | Flexible, Compliant | Complex networking |

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/FedHR5.0.git
cd FedHR5.0
```

### 2. Environment Setup

```bash
# Create environment file
cp .env.example .env

# Edit configuration
nano .env
```

### 3. Docker Compose Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f fedhr-server
```

### 4. Verify Installation

```bash
# Health check
curl http://localhost:8080/health

# Expected response
{
  "status": "healthy",
  "version": "0.1.0",
  "modules": {
    "wellbeing": "active",
    "skills": "active",
    "recruitment": "active",
    "benchmarking": "active",
    "learning": "active"
  }
}
```

## Production Deployment

### Pre-deployment Checklist

- [ ] Security audit completed
- [ ] SSL certificates obtained
- [ ] Firewall rules configured
- [ ] Backup strategy defined
- [ ] Monitoring tools ready
- [ ] Load testing performed
- [ ] Disaster recovery plan
- [ ] Privacy impact assessment

### Step-by-Step Production Setup

#### 1. Infrastructure Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
  build-essential \
  python3.9 \
  python3.9-dev \
  python3-pip \
  postgresql \
  redis-server \
  nginx \
  certbot

# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp
sudo ufw allow 50051/tcp
sudo ufw enable
```

#### 2. Database Setup

```sql
-- PostgreSQL setup
CREATE DATABASE fedhr5;
CREATE USER fedhr5_user WITH ENCRYPTED PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE fedhr5 TO fedhr5_user;

-- Enable required extensions
\c fedhr5
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

#### 3. Application Deployment

```bash
# Create application user
sudo useradd -m -s /bin/bash fedhr5

# Setup application directory
sudo mkdir -p /opt/fedhr5
sudo chown fedhr5:fedhr5 /opt/fedhr5

# Switch to app user
sudo su - fedhr5

# Clone and setup
git clone https://github.com/yourusername/FedHR5.0.git /opt/fedhr5
cd /opt/fedhr5

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

#### 4. SSL/TLS Configuration

```bash
# Obtain SSL certificate
sudo certbot certonly --standalone -d fedhr5.yourdomain.com

# Configure Nginx
sudo nano /etc/nginx/sites-available/fedhr5
```

```nginx
# /etc/nginx/sites-available/fedhr5
server {
    listen 80;
    server_name fedhr5.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name fedhr5.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/fedhr5.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/fedhr5.yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /grpc {
        grpc_pass grpc://localhost:50051;
    }
}
```

## Kubernetes Deployment

### 1. Namespace Creation

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: fedhr5
  labels:
    name: fedhr5
    environment: production
```

### 2. ConfigMaps and Secrets

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fedhr5-config
  namespace: fedhr5
data:
  PRIVACY_BUDGET: "0.1"
  MIN_CLIENTS: "2"
  LOG_LEVEL: "INFO"
  AGGREGATION_METHOD: "fedavg"
---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: fedhr5-secret
  namespace: fedhr5
type: Opaque
data:
  database-url: <base64-encoded-url>
  jwt-secret: <base64-encoded-secret>
  blockchain-key: <base64-encoded-key>
```

### 3. Deployment Manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fedhr5-server
  namespace: fedhr5
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fedhr5-server
  template:
    metadata:
      labels:
        app: fedhr5-server
    spec:
      containers:
      - name: fedhr5-server
        image: fedhr5/server:latest
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 50051
          name: grpc
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: fedhr5-secret
              key: database-url
        - name: PRIVACY_BUDGET
          valueFrom:
            configMapKeyRef:
              name: fedhr5-config
              key: PRIVACY_BUDGET
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 4. Service Configuration

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: fedhr5-server
  namespace: fedhr5
spec:
  type: LoadBalancer
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: grpc
    port: 50051
    targetPort: 50051
  selector:
    app: fedhr5-server
```

### 5. Horizontal Pod Autoscaler

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fedhr5-server-hpa
  namespace: fedhr5
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fedhr5-server
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 6. Deploy to Kubernetes

```bash
# Apply all configurations
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

# Check deployment status
kubectl get all -n fedhr5

# View logs
kubectl logs -n fedhr5 -l app=fedhr5-server -f
```

## Docker Deployment

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  fedhr-server:
    image: fedhr5/server:latest
    container_name: fedhr5-server
    restart: always
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/fedhr5
      - REDIS_URL=redis://redis:6379
      - PRIVACY_BUDGET=0.1
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - fedhr5-net
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  db:
    image: postgres:13-alpine
    container_name: fedhr5-db
    restart: always
    environment:
      - POSTGRES_DB=fedhr5
      - POSTGRES_USER=fedhr5_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - fedhr5-net

  redis:
    image: redis:6-alpine
    container_name: fedhr5-redis
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - fedhr5-net

  nginx:
    image: nginx:alpine
    container_name: fedhr5-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - fedhr-server
    networks:
      - fedhr5-net

networks:
  fedhr5-net:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

## Configuration

### Environment Variables

```bash
# Server Configuration
FEDHR_MODE=production
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
GRPC_PORT=50051

# Privacy Settings
PRIVACY_BUDGET=0.1
DELTA=1e-5
NOISE_MULTIPLIER=1.1
CLIP_NORM=1.0

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/fedhr5
REDIS_URL=redis://localhost:6379

# Security
JWT_SECRET=your-secret-key
ENCRYPTION_KEY=your-encryption-key
ENABLE_HTTPS=true

# Blockchain (optional)
BLOCKCHAIN_ENABLED=true
BLOCKCHAIN_TYPE=hyperledger
BLOCKCHAIN_ENDPOINT=http://localhost:7050

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
LOG_LEVEL=INFO
```

### Configuration File

```yaml
# config/production.yaml
server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  timeout: 300

privacy:
  epsilon: 0.1
  delta: 1e-5
  composition: advanced
  budget_manager: adaptive

modules:
  wellbeing:
    enabled: true
    update_frequency: 3600
  skills:
    enabled: true
    embedding_dim: 128
  recruitment:
    enabled: true
    bias_threshold: 0.1
  benchmarking:
    enabled: true
    min_organizations: 3
  learning:
    enabled: true
    recommendation_batch: 100

security:
  ssl_enabled: true
  auth_provider: oauth2
  session_timeout: 3600
  rate_limit: 1000

monitoring:
  metrics_endpoint: /metrics
  health_endpoint: /health
  trace_sampling: 0.1
```

## Security Hardening

### 1. Network Security

```bash
# IPTables rules
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 10 -j DROP

# Fail2ban configuration
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
```

### 2. Application Security

```python
# security_config.py
SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'",
    'Referrer-Policy': 'strict-origin-when-cross-origin'
}

# Rate limiting
RATE_LIMITS = {
    'api': '100/hour',
    'auth': '10/minute',
    'model_update': '50/day'
}
```

### 3. Data Protection

```yaml
# encryption.yaml
encryption:
  algorithm: AES-256-GCM
  key_derivation: PBKDF2
  iterations: 100000
  
data_retention:
  logs: 90 days
  models: 365 days
  user_data: GDPR compliant
  
backup:
  frequency: daily
  encryption: enabled
  offsite: true
```

## Monitoring & Observability

### 1. Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'fedhr5-server'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
    
  - job_name: 'fedhr5-clients'
    file_sd_configs:
      - files:
        - '/etc/prometheus/clients/*.json'
        
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']

rule_files:
  - 'alerts.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']
```

### 2. Grafana Dashboards

```json
{
  "dashboard": {
    "title": "FedHR5.0 Monitoring",
    "panels": [
      {
        "title": "Privacy Budget Usage",
        "targets": [{
          "expr": "fedhr5_privacy_budget_spent"
        }]
      },
      {
        "title": "Model Performance",
        "targets": [{
          "expr": "fedhr5_model_accuracy"
        }]
      },
      {
        "title": "Active Clients",
        "targets": [{
          "expr": "fedhr5_active_clients"
        }]
      }
    ]
  }
}
```

### 3. Logging Configuration

```python
# logging_config.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/fedhr5/app.log',
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'privacy_audit': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/fedhr5/privacy_audit.log',
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 30,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'fedhr5': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'fedhr5.privacy': {
            'handlers': ['privacy_audit'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

## Troubleshooting

### Common Issues

#### 1. Connection Refused

```bash
# Check if services are running
docker-compose ps
systemctl status fedhr5

# Check ports
netstat -tlnp | grep -E '8080|50051'

# Check firewall
sudo ufw status
```

#### 2. Privacy Budget Exceeded

```python
# Reset privacy budget (development only!)
from fedhr5.privacy import PrivacyBudgetManager

manager = PrivacyBudgetManager()
manager.reset_budget()  # WARNING: Only in development
```

#### 3. Performance Issues

```bash
# Check resource usage
htop
docker stats

# Analyze slow queries
psql -U fedhr5_user -d fedhr5 -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"

# Profile Python code
python -m cProfile -o profile.stats app.py
```

### Debug Mode

```bash
# Enable debug logging
export FEDHR_DEBUG=true
export LOG_LEVEL=DEBUG

# Run with verbose output
python -m fedhr5.server --verbose --debug
```

## Maintenance

### Backup Procedures

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/fedhr5"

# Database backup
pg_dump -U fedhr5_user fedhr5 | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Redis backup
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# Model backup
tar -czf $BACKUP_DIR/models_$DATE.tar.gz /opt/fedhr5/models/

# Encrypt backups
gpg --encrypt --recipient backup@fedhr5.org $BACKUP_DIR/*_$DATE.*
```

### Update Procedures

```bash
# 1. Backup current version
./scripts/backup.sh

# 2. Pull latest changes
cd /opt/fedhr5
git pull origin main

# 3. Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Restart services
sudo systemctl restart fedhr5
```

### Health Checks

```python
# health_check.py
import requests
import sys

def check_health():
    try:
        response = requests.get('http://localhost:8080/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'healthy':
                print("✅ System healthy")
                return 0
        print("⚠️ System unhealthy")
        return 1
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return 2

if __name__ == "__main__":
    sys.exit(check_health())
```

## Support

For deployment assistance:
- 📧 Email: support@fedhr5.org
- 💬 Slack: fedhr5.slack.com
- 📚 Documentation: docs.fedhr5.org

---

*Last Updated: December 2024*
*Version: 0.1.0*