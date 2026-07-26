# Setup Guide

## Prerequisites

- Node.js 18+ ([Download](https://nodejs.org))
- Python 3.9+ ([Download](https://www.python.org))
- Docker & Docker Compose ([Download](https://www.docker.com))
- Git ([Download](https://git-scm.com))

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/mr-Arun-2006/finance-pwa-ai.git
cd finance-pwa-ai
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Update .env with your configuration
# nano .env

# Run migrations (if using Prisma)
npm run migrate

# Start development server
npm run dev
```

Backend will be available at `http://localhost:3001`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Update .env with your configuration
# nano .env

# Start development server
npm start
```

Frontend will be available at `http://localhost:3000`

### 4. ML Service Setup

```bash
cd ml-models

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train models (optional)
python src/model_trainer.py

# Start ML service
python -m uvicorn src.main:app --reload
```

ML service will be available at `http://localhost:5000`

## Docker Compose Setup (Recommended)

### Start All Services

```bash
# From project root
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Backend API (port 3001)
- ML service (port 5000)
- Frontend (port 3000)
- Nginx reverse proxy (port 80)

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

### Stop Services

```bash
docker-compose down
```

### Remove Data

```bash
# Remove all volumes (databases, caches)
docker-compose down -v
```

## Environment Variables

### Backend (.env)

```env
# Server
NODE_ENV=development
PORT=3001

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/finance_pwa

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your_super_secret_key
JWT_EXPIRY=7d

# Bank APIs
PLAID_CLIENT_ID=your_id
PLAID_SECRET=your_secret

# ML Service
ML_SERVICE_URL=http://localhost:5000
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:3001
REACT_APP_ML_URL=http://localhost:5000
REACT_APP_ENV=development
```

## Database Setup

### PostgreSQL

1. Create database:

```bash
createdb finance_pwa
```

2. Run migrations:

```bash
npm run migrate
```

### Redis

Redis will be started automatically with Docker Compose.

For local setup:
```bash
# macOS
brew install redis
redis-server

# Ubuntu
sudo apt-get install redis-server
redis-server
```

## Verification

Verify all services are running:

```bash
# Backend health
curl http://localhost:3001/health

# ML service health
curl http://localhost:5000/health

# Frontend
open http://localhost:3000
```

## Troubleshooting

### Port Already in Use

```bash
# Kill process on specific port (macOS/Linux)
lsof -i :3001
kill -9 <PID>

# On Windows
netstat -ano | findstr :3001
taskkill /PID <PID> /F
```

### Database Connection Error

```bash
# Check PostgreSQL is running
psql -U postgres

# Or with Docker
docker-compose logs postgres
```

### Python Virtual Environment Issues

```bash
# Reinstall virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. Configure authentication
2. Set up bank API integrations
3. Train ML models with your data
4. Deploy to production
