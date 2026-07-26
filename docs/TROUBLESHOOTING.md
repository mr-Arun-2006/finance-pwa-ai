# Troubleshooting Guide

## Common Issues

### Frontend Issues

#### Blank page displayed

**Cause**: Backend API not responding

**Solution**:
```bash
# Check backend status
curl http://localhost:3001/health

# Restart backend
docker-compose restart backend
```

#### "Cannot GET /" error

**Cause**: Frontend not built

**Solution**:
```bash
cd frontend
npm install
npm start
```

#### CORS errors

**Cause**: CORS not properly configured

**Solution**:
```typescript
// backend/src/server.ts
app.use(cors({
  origin: process.env.FRONTEND_URL,
  credentials: true
}));
```

### Backend Issues

#### Database connection error

**Cause**: PostgreSQL not running or connection string wrong

**Solution**:
```bash
# Check database connection
pg_isready -h localhost -U finance_user

# Update .env
DATABASE_URL=postgresql://finance_user:password@localhost:5432/finance_pwa
```

#### "Port already in use"

**Cause**: Another process using the port

**Solution**:
```bash
# Kill process on port 3001
kill -9 $(lsof -ti:3001)

# Or use different port
PORT=3002 npm run dev
```

#### JWT token errors

**Cause**: Invalid or expired token

**Solution**:
```bash
# Generate new JWT secret
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Update .env
JWT_SECRET=<new-secret>
```

### ML Service Issues

#### Model not found

**Cause**: Models not trained

**Solution**:
```bash
cd ml-models
python src/model_trainer.py
```

#### Slow predictions

**Cause**: Large batch size or insufficient resources

**Solution**:
```python
# Reduce batch size
for i in range(0, len(transactions), 32):  # Changed from 100
    batch = transactions[i:i+32]
    predictions = model.predict_batch(batch)
```

#### Out of memory

**Cause**: Large dataset in memory

**Solution**:
```bash
# Increase memory limit
docker-compose.yml:
  ml-service:
    mem_limit: 4g
```

### Docker Issues

#### Container exits immediately

**Cause**: Application error

**Solution**:
```bash
# Check logs
docker logs <container-id>

# Or with compose
docker-compose logs backend
```

#### Cannot connect to Docker daemon

**Cause**: Docker not running or permission issue

**Solution**:
```bash
# Start Docker
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
```

#### Image build fails

**Cause**: Dockerfile error or missing dependencies

**Solution**:
```bash
# Clean build
docker-compose build --no-cache

# Check Dockerfile syntax
docker build -t test .
```

### Performance Issues

#### High CPU usage

**Cause**: Inefficient queries or calculations

**Solution**:
```bash
# Monitor CPU
docker stats backend

# Check slow queries
ENABLE_QUERY_LOGGING=true npm run dev
```

#### High memory usage

**Cause**: Memory leak or large data structures

**Solution**:
```bash
# Monitor memory
docker stats

# Restart service
docker-compose restart backend
```

#### Slow API responses

**Cause**: Database queries or missing indexes

**Solution**:
```sql
-- Add indexes
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_user ON transactions(user_id, date);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM transactions WHERE date > NOW() - INTERVAL '30 days';
```

## Debug Mode

### Enable verbose logging

**Backend**:
```bash
DEBUG=* npm run dev
```

**Frontend**:
```bash
REACT_APP_DEBUG=true npm start
```

**ML Service**:
```bash
DEBUG=1 python -m uvicorn src.main:app --reload
```

## Getting Help

1. Check this troubleshooting guide
2. Search GitHub issues
3. Check Docker logs
4. Review error messages carefully
5. Create GitHub issue with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Log excerpts

## Reporting Bugs

Include:
- OS and version
- Node.js/Python version
- Docker version
- Exact error message
- Steps to reproduce
- Expected vs actual behavior
