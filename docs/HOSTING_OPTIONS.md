# Hosting Options for Finance PWA

This guide covers multiple hosting platforms for your Finance PWA application.

## Option 1: DigitalOcean (Recommended for Beginners)

### Step 1: Create a Droplet

1. Go to [DigitalOcean](https://www.digitalocean.com)
2. Create account and add payment method
3. Click "Create" → "Droplets"
4. Choose:
   - Image: Ubuntu 22.04 LTS
   - Size: $12/month (2GB RAM, 2 vCPU)
   - Region: Closest to you
   - Authentication: SSH key
5. Click "Create Droplet"

### Step 2: Connect to Your Droplet

```bash
ssh root@your_droplet_ip
```

### Step 3: Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

# Install Python
apt install -y python3.9 python3-pip python3-venv

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker root

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### Step 4: Clone and Deploy

```bash
cd /opt
git clone https://github.com/mr-Arun-2006/finance-pwa-ai.git
cd finance-pwa-ai

# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Update environment variables
nano backend/.env
nano frontend/.env

# Build and start
docker-compose up -d

# Check status
docker-compose ps
```

### Step 5: Set Up Domain (Optional)

1. Point your domain's A record to the Droplet IP
2. Install Certbot for SSL:

```bash
apt install -y certbot python3-certbot-nginx
certbot certonly --standalone -d yourdomain.com
```

### Step 6: Access Your App

- Frontend: `http://your_droplet_ip:3000`
- Backend API: `http://your_droplet_ip:3001`
- ML Service: `http://your_droplet_ip:5000`

**Cost**: $12-24/month

---

## Option 2: AWS (Scalable)

### Using EC2 + RDS + ElastiCache

#### Step 1: Create EC2 Instance

1. Go to [AWS Console](https://console.aws.amazon.com)
2. EC2 → Instances → Launch Instance
3. Choose:
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t3.small
   - Security group: Allow ports 80, 443, 3000, 3001, 5000
4. Create and download key pair

#### Step 2: Connect via SSH

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### Step 3: Install Docker

```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

#### Step 4: Create RDS PostgreSQL

1. RDS → Databases → Create database
2. Engine: PostgreSQL 15
3. DB instance identifier: finance-pwa-db
4. Master username: admin
5. Auto generate password or set custom
6. DB instance class: db.t3.micro
7. Storage: 20 GB
8. Create

#### Step 5: Create ElastiCache Redis

1. ElastiCache → Clusters → Create
2. Cluster engine: Redis
3. Node type: cache.t3.micro
4. Number of nodes: 1
5. Create

#### Step 6: Deploy Application

```bash
cd /home/ubuntu
git clone https://github.com/mr-Arun-2006/finance-pwa-ai.git
cd finance-pwa-ai

# Create .env files with RDS and ElastiCache endpoints
cat > backend/.env << EOF
NODE_ENV=production
PORT=3001
DATABASE_URL=postgresql://admin:password@rds-endpoint:5432/finance_pwa
REDIS_URL=redis://elasticache-endpoint:6379
JWT_SECRET=$(openssl rand -hex 32)
ML_SERVICE_URL=http://localhost:5000
EOF

# Start application
docker-compose up -d
```

#### Step 7: Configure Domain with Route 53

1. Route 53 → Hosted zones → Create hosted zone
2. Add A record pointing to EC2 instance
3. Use ACM for SSL certificate

**Cost**: $20-50+/month (scales with usage)

---

## Option 3: Heroku (Easiest, Limited Free Tier)

### Step 1: Install Heroku CLI

```bash
npm install -g heroku
heroku login
```

### Step 2: Create Heroku App

```bash
heroku create your-finance-pwa
```

### Step 3: Add Buildpacks

```bash
heroku buildpacks:add heroku/nodejs
heroku buildpacks:add heroku/python
```

### Step 4: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:basic
```

### Step 5: Deploy

```bash
git push heroku main
```

### Step 6: Configure Environment

```bash
heroku config:set JWT_SECRET=$(openssl rand -hex 32)
heroku config:set NODE_ENV=production
```

**Note**: Heroku has limited free offerings. Paid plans start at $7/month per dyno.

---

## Option 4: Railway (Modern & Simple)

### Step 1: Create Account

1. Go to [Railway](https://railway.app)
2. Sign up with GitHub

### Step 2: Connect Repository

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose finance-pwa-ai
4. Authorize Railway

### Step 3: Add Services

1. PostgreSQL plugin
2. Redis plugin
3. Configure environment variables

### Step 4: Deploy

Railway automatically detects Dockerfile and deploys:

```
Frontend: https://your-project.railway.app:3000
Backend: https://your-project.railway.app:3001
ML: https://your-project.railway.app:5000
```

**Cost**: Pay as you go, typically $5-20/month

---

## Option 5: Google Cloud Run (Serverless)

### Step 1: Install Google Cloud CLI

```bash
curl https://sdk.cloud.google.com | bash
gcloud init
```

### Step 2: Create Project

```bash
gcloud projects create finance-pwa
gcloud config set project finance-pwa
```

### Step 3: Enable APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudsql.googleapis.com
```

### Step 4: Deploy Backend

```bash
cd backend
gcloud run deploy finance-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars NODE_ENV=production
```

### Step 5: Deploy ML Service

```bash
cd ../ml-models
gcloud run deploy finance-ml \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 1Gi
```

**Cost**: Free tier included, then $0.00002400 per CPU-second

---

## Option 6: GitHub Pages + Vercel (Frontend Only)

### Deploy Frontend to Vercel

```bash
npm i -g vercel
vercel login
vercel --prod
```

### Deploy Backend to Railway/Heroku

Deploy backend separately to Railway or Heroku, then update frontend `.env` to point to backend URL.

---

## Comparison Table

| Platform | Cost | Difficulty | Scalability | Best For |
|----------|------|-----------|------------|----------|
| DigitalOcean | $12/mo | Easy | Good | Startups |
| AWS | $20+/mo | Medium | Excellent | Enterprise |
| Heroku | $7/mo | Very Easy | Limited | Rapid prototyping |
| Railway | $5/mo | Easy | Good | Indie projects |
| Google Cloud Run | Free tier | Medium | Excellent | Serverless |
| Vercel + Railway | $5+/mo | Easy | Good | Full-stack |

---

## Post-Deployment Checklist

- [ ] Change default passwords
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring & alerts
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Enable security headers
- [ ] Test all endpoints
- [ ] Set up logging
- [ ] Configure firewall rules
- [ ] Document deployment process

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check all services
curl https://yourdomain.com/api/health
curl https://yourdomain.com/ml/health
```

### Enable Monitoring

#### DataDog (Free tier)
```bash
docker run -d \
  -e DD_AGENT_MAJOR_VERSION=7 \
  -e DD_API_KEY=your_api_key \
  datadog/agent:latest
```

#### Prometheus + Grafana
```bash
docker-compose -f monitoring.yml up -d
```

### Backup Strategy

```bash
# Daily database backups
0 2 * * * pg_dump $DATABASE_URL | gzip > /backups/db_$(date +%Y%m%d).sql.gz
```

---

## Troubleshooting Deployment

### Port Already in Use
```bash
# Change port in docker-compose.yml or cloud config
```

### Database Connection Issues
```bash
# Test connection
psql $DATABASE_URL
```

### Out of Memory
```bash
# Increase container limits
# docker-compose.yml:
# services:
#   backend:
#     mem_limit: 512m
```

### SSL Certificate Issues
```bash
# Renew certificate
certbot renew
```

---

## Next Steps

1. Choose a platform from above
2. Follow the specific deployment guide
3. Test all endpoints
4. Set up monitoring
5. Configure backups
6. Monitor costs

For questions, check the [Troubleshooting Guide](./TROUBLESHOOTING.md).
