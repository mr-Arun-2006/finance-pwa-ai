# Deployment Guide

## Production Deployment

### Prerequisites

- AWS/Azure/DigitalOcean account
- Docker & Docker Compose installed
- Domain name
- SSL certificate
- Database backup strategy

## Option 1: Docker Compose on VPS

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Clone Repository

```bash
cd /opt
sudo git clone https://github.com/mr-Arun-2006/finance-pwa-ai.git
cd finance-pwa-ai
```

### 3. Configure Environment

```bash
# Create production .env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit with production values
sudo nano backend/.env
sudo nano frontend/.env
```

**Backend .env (Production)**

```env
NODE_ENV=production
PORT=3001

DATABASE_URL=postgresql://user:password@postgres:5432/finance_pwa
REDIS_URL=redis://redis:6379

JWT_SECRET=<generate-secure-key>
JWT_EXPIRY=7d

ML_SERVICE_URL=http://ml-service:5000

# Plaid API
PLAID_CLIENT_ID=<your-id>
PLAID_SECRET=<your-secret>

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<your-email>
SMTP_PASS=<your-app-password>
```

### 4. Start Services

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Verify
docker-compose ps
```

### 5. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Update nginx config
sudo nano docker/nginx.conf
```

**nginx.conf (SSL)**

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... rest of config
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### 6. Database Backups

```bash
#!/bin/bash
# backup.sh - Daily backup script

BACKUP_DIR="/backups/postgres"
DATABASE_URL="postgresql://user:password@localhost:5432/finance_pwa"

DATE=$(date +%Y-%m-%d_%H-%M-%S)

# Backup
pg_dump $DATABASE_URL | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

```bash
# Add to crontab
0 2 * * * /opt/finance-pwa-ai/backup.sh
```

## Option 2: Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (EKS, AKS, GKE)
- kubectl configured
- Helm installed

### 1. Create Namespace

```bash
kubectl create namespace finance-pwa
```

### 2. Create Secrets

```bash
kubectl create secret generic finance-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=JWT_SECRET="..." \
  -n finance-pwa
```

### 3. Deploy PostgreSQL

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql \
  --set auth.postgresPassword=password \
  --set auth.username=financeuser \
  --set auth.password=password \
  --set auth.database=finance_pwa \
  -n finance-pwa
```

### 4. Deploy Backend

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: finance-backend
  namespace: finance-pwa
spec:
  replicas: 3
  selector:
    matchLabels:
      app: finance-backend
  template:
    metadata:
      labels:
        app: finance-backend
    spec:
      containers:
      - name: backend
        image: your-registry/finance-backend:latest
        ports:
        - containerPort: 3001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: finance-secrets
              key: DATABASE_URL
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: finance-secrets
              key: JWT_SECRET
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3001
          initialDelaySeconds: 30
          periodSeconds: 10
```

```bash
kubectl apply -f backend-deployment.yaml
```

### 5. Create Service

```yaml
# backend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: finance-backend
  namespace: finance-pwa
spec:
  selector:
    app: finance-backend
  ports:
  - port: 3001
    targetPort: 3001
  type: LoadBalancer
```

## Option 3: AWS Deployment

### Using ECS Fargate

```bash
# Create ECR repositories
aws ecr create-repository --repository-name finance-backend
aws ecr create-repository --repository-name finance-frontend
aws ecr create-repository --repository-name finance-ml

# Push images
docker tag finance-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/finance-backend:latest
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/finance-backend:latest
```

### RDS for PostgreSQL

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier finance-pwa-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password "YourStrongPassword123!" \
  --allocated-storage 20
```

## Monitoring

### Docker Monitoring

```bash
# View container stats
docker stats

# View logs
docker-compose logs -f backend
```

### Health Checks

```bash
# Backend
curl https://yourdomain.com/api/health

# Frontend
curl https://yourdomain.com

# ML Service
curl https://yourdomain.com/ml/health
```

### Prometheus + Grafana

```yaml
# docker-compose.yml additions
  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
```

## Auto-Scaling

### Kubernetes HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: finance-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: finance-backend
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

## Troubleshooting

### Container Won't Start

```bash
docker logs <container-id>
```

### Database Connection Issues

```bash
# Check database
docker-compose exec postgres psql -U finance_user -d finance_pwa
```

### High Memory Usage

```bash
# Restart services
docker-compose restart

# Clean up
docker system prune -a
```

## Performance Tuning

### Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_category ON transactions(category);
```

### Redis Optimization

```bash
# Set memory policy
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Node.js Optimization

```bash
# Set worker processes based on CPU cores
NODE_ENV=production node --max_old_space_size=4096 server.js
```
