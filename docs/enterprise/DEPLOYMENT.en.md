# Deployment Guide - UltimatePro Advance Enterprise

Production deployment guide for ABTPro UltimatePro Advance Enterprise Edition.

## Table of Contents

1. [Deployment Options](#deployment-options)
2. [Cloud Deployment](#cloud-deployment)
3. [On-Premise Deployment](#on-premise-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [High Availability Setup](#high-availability-setup)
7. [Security Hardening](#security-hardening)
8. [Backup & Recovery](#backup--recovery)
9. [Monitoring Setup](#monitoring-setup)
10. [Post-Deployment Checklist](#post-deployment-checklist)

## Deployment Options

### Comparison Matrix

| Feature | Cloud Hosted | On-Premise | Hybrid |
|---------|-------------|------------|--------|
| Setup Time | 1-2 hours | 1-2 days | 2-3 days |
| Initial Cost | Low | High | Medium |
| Ongoing Cost | Medium | Low | Medium |
| Control | Medium | High | High |
| Scalability | High | Medium | High |
| Maintenance | Managed | Self-managed | Shared |

### Recommended Deployment

**For Most Organizations:** Cloud Hosted + Multi-Region
**For Regulated Industries:** On-Premise with DR in Cloud
**For High-Volume Trading:** Kubernetes Cluster (Cloud or On-Prem)

## Cloud Deployment

### AWS Deployment

#### Prerequisites

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
```

#### Infrastructure Setup

**1. Create VPC and Networking:**

```bash
# Create VPC
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=abtpro-vpc}]'

# Create subnets
aws ec2 create-subnet \
  --vpc-id vpc-xxxxx \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

aws ec2 create-subnet \
  --vpc-id vpc-xxxxx \
  --cidr-block 10.0.2.0/24 \
  --availability-zone us-east-1b
```

**2. Launch RDS for Database:**

```bash
aws rds create-db-instance \
  --db-instance-identifier abtpro-db \
  --db-instance-class db.r5.2xlarge \
  --engine postgres \
  --engine-version 15.3 \
  --master-username abtpro \
  --master-user-password <secure-password> \
  --allocated-storage 500 \
  --storage-type gp3 \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name abtpro-subnet-group \
  --backup-retention-period 30 \
  --multi-az
```

**3. Launch ElastiCache for Redis:**

```bash
aws elasticache create-replication-group \
  --replication-group-id abtpro-redis \
  --replication-group-description "ABTPro Redis Cluster" \
  --engine redis \
  --engine-version 7.0 \
  --cache-node-type cache.r5.xlarge \
  --num-cache-clusters 3 \
  --automatic-failover-enabled \
  --multi-az-enabled
```

**4. Launch EC2 Instances:**

```bash
# Launch application servers
aws ec2 run-instances \
  --image-id ami-xxxxx \
  --instance-type c5.4xlarge \
  --count 3 \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx \
  --key-name abtpro-key \
  --user-data file://install-script.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=abtpro-app}]'
```

**5. Configure Load Balancer:**

```bash
# Create Application Load Balancer
aws elbv2 create-load-balancer \
  --name abtpro-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx \
  --scheme internet-facing

# Create target group
aws elbv2 create-target-group \
  --name abtpro-targets \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxxxx \
  --health-check-path /health
```

#### Terraform Configuration (Alternative)

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "abtpro" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = {
    Name = "abtpro-vpc"
  }
}

# RDS Instance
resource "aws_db_instance" "abtpro" {
  identifier = "abtpro-db"
  engine = "postgres"
  engine_version = "15.3"
  instance_class = "db.r5.2xlarge"
  allocated_storage = 500
  storage_type = "gp3"
  
  db_name = "abtpro_enterprise"
  username = "abtpro"
  password = var.db_password
  
  multi_az = true
  backup_retention_period = 30
  backup_window = "03:00-04:00"
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name = aws_db_subnet_group.abtpro.name
  
  tags = {
    Name = "abtpro-database"
  }
}

# ElastiCache Redis
resource "aws_elasticache_replication_group" "abtpro" {
  replication_group_id = "abtpro-redis"
  replication_group_description = "ABTPro Redis Cluster"
  
  engine = "redis"
  engine_version = "7.0"
  node_type = "cache.r5.xlarge"
  number_cache_clusters = 3
  
  automatic_failover_enabled = true
  multi_az_enabled = true
  
  subnet_group_name = aws_elasticache_subnet_group.abtpro.name
  security_group_ids = [aws_security_group.redis.id]
}

# Auto Scaling Group
resource "aws_autoscaling_group" "abtpro" {
  name = "abtpro-asg"
  min_size = 3
  max_size = 10
  desired_capacity = 3
  
  vpc_zone_identifier = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]
  
  launch_template {
    id = aws_launch_template.abtpro.id
    version = "$Latest"
  }
  
  target_group_arns = [aws_lb_target_group.abtpro.arn]
  
  health_check_type = "ELB"
  health_check_grace_period = 300
}
```

Deploy with Terraform:
```bash
terraform init
terraform plan
terraform apply
```

### Google Cloud Platform (GCP)

#### Setup with gcloud

```bash
# Create project
gcloud projects create abtpro-production

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable redis.googleapis.com

# Create Cloud SQL instance
gcloud sql instances create abtpro-db \
  --database-version=POSTGRES_15 \
  --tier=db-custom-8-32768 \
  --region=us-central1 \
  --availability-type=REGIONAL \
  --backup-start-time=03:00

# Create Redis instance
gcloud redis instances create abtpro-redis \
  --size=5 \
  --region=us-central1 \
  --tier=standard \
  --redis-version=redis_7_0

# Create GKE cluster
gcloud container clusters create abtpro-cluster \
  --region=us-central1 \
  --num-nodes=3 \
  --machine-type=n2-standard-8 \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=10
```

### Azure Deployment

```bash
# Create resource group
az group create \
  --name abtpro-rg \
  --location eastus

# Create PostgreSQL server
az postgres flexible-server create \
  --resource-group abtpro-rg \
  --name abtpro-db \
  --location eastus \
  --admin-user abtpro \
  --admin-password <password> \
  --sku-name Standard_D8s_v3 \
  --tier GeneralPurpose \
  --high-availability Enabled

# Create Redis cache
az redis create \
  --resource-group abtpro-rg \
  --name abtpro-redis \
  --location eastus \
  --sku Premium \
  --vm-size P3

# Create AKS cluster
az aks create \
  --resource-group abtpro-rg \
  --name abtpro-cluster \
  --node-count 3 \
  --node-vm-size Standard_D8s_v3 \
  --enable-cluster-autoscaler \
  --min-count 3 \
  --max-count 10
```

## On-Premise Deployment

### Hardware Requirements

**Minimum Production Setup:**
- **Application Servers**: 3x servers, 16 cores, 64GB RAM each
- **Database Server**: 1x server, 32 cores, 128GB RAM, RAID 10 SSD
- **Load Balancer**: 2x servers, 8 cores, 16GB RAM each
- **Network**: 10 Gbps internal, redundant internet connections

### Installation Steps

**1. Prepare Servers:**

```bash
# Update all servers
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**2. Setup Database Server:**

```bash
# Install PostgreSQL 15
sudo apt-get install postgresql-15 postgresql-contrib-15

# Configure PostgreSQL
sudo nano /etc/postgresql/15/main/postgresql.conf
# Apply production settings from Configuration Guide

# Configure replication
sudo nano /etc/postgresql/15/main/pg_hba.conf
# Add replication entries

# Restart PostgreSQL
sudo systemctl restart postgresql
```

**3. Deploy Application:**

```bash
# Clone repository on each app server
git clone https://github.com/ZeaZDev/ABTPi18n.git
cd ABTPi18n

# Configure environment
cp .env.enterprise.example .env
nano .env  # Edit with production settings

# Deploy
docker-compose -f docker-compose.enterprise.prod.yml up -d
```

**4. Configure Load Balancer (HAProxy):**

```bash
# Install HAProxy
sudo apt-get install haproxy

# Configure
sudo nano /etc/haproxy/haproxy.cfg
```

**HAProxy Configuration:**
```cfg
global
    log /dev/log local0
    maxconn 4096
    
defaults
    log global
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend abtpro_frontend
    bind *:443 ssl crt /etc/ssl/certs/abtpro.pem
    default_backend abtpro_backend

backend abtpro_backend
    balance roundrobin
    option httpchk GET /health
    server app1 192.168.1.11:8000 check
    server app2 192.168.1.12:8000 check
    server app3 192.168.1.13:8000 check
```

## Docker Deployment

### Production Docker Compose

```yaml
version: '3.8'

services:
  backend:
    image: abtpro/backend:enterprise-latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    networks:
      - abtpro_network
    depends_on:
      - postgres
      - redis

  worker:
    image: abtpro/worker:enterprise-latest
    deploy:
      replicas: 5
      resources:
        limits:
          cpus: '2'
          memory: 4G
    environment:
      - CELERY_BROKER_URL=${REDIS_URL}/1
      - CELERY_RESULT_BACKEND=${REDIS_URL}/2
    networks:
      - abtpro_network

  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=abtpro_enterprise
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    networks:
      - abtpro_network

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - abtpro_network

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - abtpro_network

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    networks:
      - abtpro_network

networks:
  abtpro_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

## Kubernetes Deployment

### Kubernetes Manifests

**Namespace:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: abtpro
```

**Backend Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: abtpro-backend
  namespace: abtpro
spec:
  replicas: 3
  selector:
    matchLabels:
      app: abtpro-backend
  template:
    metadata:
      labels:
        app: abtpro-backend
    spec:
      containers:
      - name: backend
        image: abtpro/backend:enterprise-latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: abtpro-secrets
              key: database-url
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Service:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: abtpro-backend
  namespace: abtpro
spec:
  selector:
    app: abtpro-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Horizontal Pod Autoscaler:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: abtpro-backend-hpa
  namespace: abtpro
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: abtpro-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n abtpro
kubectl get services -n abtpro

# Check logs
kubectl logs -f deployment/abtpro-backend -n abtpro
```

## High Availability Setup

### Active-Active Configuration

**Database Replication:**
```bash
# On primary database
psql -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'password';"

# Configure primary
# In postgresql.conf:
wal_level = replica
max_wal_senders = 3
wal_keep_size = 1GB

# On replica
# In recovery.conf:
standby_mode = 'on'
primary_conninfo = 'host=primary_host port=5432 user=replicator password=password'
```

**Redis Sentinel:**
```bash
# sentinel.conf
sentinel monitor abtpro-master 192.168.1.10 6379 2
sentinel down-after-milliseconds abtpro-master 5000
sentinel failover-timeout abtpro-master 10000
sentinel parallel-syncs abtpro-master 1

# Start sentinel
redis-sentinel /etc/redis/sentinel.conf
```

## Security Hardening

### SSL/TLS Configuration

```bash
# Generate SSL certificate (use Let's Encrypt for production)
sudo certbot certonly --standalone -d api.abtpro.com

# Configure Nginx with SSL
server {
    listen 443 ssl http2;
    server_name api.abtpro.com;
    
    ssl_certificate /etc/letsencrypt/live/api.abtpro.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.abtpro.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    add_header Strict-Transport-Security "max-age=31536000" always;
}
```

### Firewall Rules

```bash
# UFW (Ubuntu)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 80/tcp    # HTTP (redirect to HTTPS)
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -P INPUT DROP
```

## Backup & Recovery

### Automated Backups

```bash
#!/bin/bash
# /usr/local/bin/backup-abtpro.sh

BACKUP_DIR="/backups/abtpro"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump -h localhost -U abtpro abtpro_enterprise | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Backup Redis
redis-cli --rdb "$BACKUP_DIR/redis_$DATE.rdb"

# Upload to S3
aws s3 cp "$BACKUP_DIR/" s3://abtpro-backups/ --recursive

# Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -mtime +30 -delete
```

**Schedule with cron:**
```bash
# Edit crontab
crontab -e

# Add backup job (daily at 2 AM)
0 2 * * * /usr/local/bin/backup-abtpro.sh
```

## Monitoring Setup

### Prometheus Configuration

See [Configuration Guide](CONFIGURATION.en.md#monitoring-configuration)

### Alerting Rules

```yaml
# prometheus-alerts.yml
groups:
- name: abtpro
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 5m
    annotations:
      summary: "High error rate detected"
  
  - alert: DatabaseDown
    expr: up{job="postgres"} == 0
    for: 1m
    annotations:
      summary: "Database is down"
  
  - alert: HighMemoryUsage
    expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.90
    for: 5m
    annotations:
      summary: "Memory usage above 90%"
```

## Post-Deployment Checklist

- [ ] All services running and healthy
- [ ] Database migrations completed
- [ ] SSL certificates installed and valid
- [ ] Firewall rules configured
- [ ] Backups configured and tested
- [ ] Monitoring dashboards accessible
- [ ] Alerts configured and tested
- [ ] Load balancer health checks passing
- [ ] API endpoints responding
- [ ] WebSocket connections working
- [ ] Exchange connections verified
- [ ] Test bot executed successfully
- [ ] Disaster recovery plan documented
- [ ] Team access configured
- [ ] Documentation updated

---

*Congratulations! Your ABTPro UltimatePro Advance Enterprise deployment is complete.*

*For ongoing support: enterprise@abtpro.com*
