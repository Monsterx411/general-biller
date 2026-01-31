# Quick Start Deployment Guide

## 🚀 Fast Track to Deployment

### Option A: Local Development (Fastest - 2 minutes)
```bash
# 1. Install dependencies
source .venv/bin/activate
pip install -r requirements.txt

# 2. Set environment variable
export SECRET_KEY="your-32-character-secret-key-here123456"

# 3. Run the app
python main.py

# 4. Test
curl http://localhost:5000/health
```
✅ App runs on `http://localhost:5000`

---

### Option B: Docker Container (5 minutes - Recommended)
```bash
# 1. Build Docker image
docker build -t general-biller:latest .

# 2. Run container with environment variables
docker run -d \
  --name biller \
  -p 5000:5000 \
  -e SECRET_KEY="your-secret-key" \
  -e ENVIRONMENT="production" \
  -v $(pwd)/data:/app/data \
  general-biller:latest

# 3. View logs
docker logs -f biller

# 4. Test
curl http://localhost:5000/health
```
✅ App runs in container on `http://localhost:5000`

---

### Option C: Docker Compose (5 minutes - Best for Production)
```bash
# 1. Start all services (app + database)
docker-compose up -d

# 2. View logs
docker-compose logs -f app

# 3. Test
curl http://localhost:5000/health

# 4. Monitor
docker-compose ps
```
✅ Full stack running with PostgreSQL database

---

### Option D: GitHub Actions Automatic Deployment

**Already configured!** Your workflow deploys automatically when:
1. You push to `main` branch
2. All tests pass ✅
3. Docker build succeeds ✅
4. Deploy job runs ✅

**To trigger deployment:**
```bash
git add .
git commit -m "Deploy update"
git push origin main
```
Then watch: GitHub → Actions tab → See deploy job run

---

## 🔧 Configuration

### Required Environment Variables
```bash
# Minimum required
export SECRET_KEY="your-32-character-key-minimum"
export ENVIRONMENT="production"  # or "development"

# Optional with defaults
export DATABASE_URL="sqlite:///loan_manager.db"  # or PostgreSQL
export APP_PORT="5000"
export LOG_LEVEL="INFO"
```

### Create .env file (for local/container use)
```bash
cat > .env << EOF
SECRET_KEY=your-secret-key-here-must-be-32-chars-minimum123456
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@localhost:5432/biller
APP_PORT=5000
LOG_LEVEL=INFO
ALLOW_ORIGINS=http://localhost:3000,https://yourdomain.com
EOF
```

---

## 📊 Verify Deployment

### Health Check Endpoints
```bash
# Basic health check
curl http://localhost:5000/health

# Detailed readiness check  
curl http://localhost:5000/readiness

# API test - Get personal loans
curl -X GET http://localhost:5000/api/v1/personal/loans \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### View Logs
```bash
# Docker logs
docker logs biller

# System logs (if using systemd)
sudo journalctl -u biller -f

# Docker Compose logs
docker-compose logs -f app

# File logs
tail -f /var/log/biller/error.log
```

---

## 🛠️ Database Setup

### SQLite (Default - No Setup Needed)
- Uses file-based database
- Perfect for development
- Data persists in `loan_manager.db`

### PostgreSQL (Production)
```bash
# 1. Install PostgreSQL
brew install postgresql  # macOS
apt-get install postgresql  # Linux

# 2. Create database
createdb general_biller

# 3. Set connection string
export DATABASE_URL="postgresql://user:password@localhost:5432/general_biller"

# 4. Run migrations
alembic upgrade head

# 5. Verify
psql general_biller -c "SELECT version();"
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Port 5000 already in use" | `lsof -i :5000` then `kill -9 <PID>` or use different port |
| "SECRET_KEY too short" | Ensure 32+ characters: `openssl rand -hex 16` |
| "Database connection failed" | Check `DATABASE_URL` and that database is running |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Permission denied deploy.sh" | Run `chmod +x deploy.sh` |
| "Docker not found" | Install Docker from docker.com |

---

## 📋 Pre-Deployment Checklist

- [ ] Tests passing: `pytest tests/ -v`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file configured with all required variables
- [ ] Database migrations run: `alembic upgrade head`
- [ ] Health endpoint responds: `curl http://localhost:5000/health`
- [ ] API endpoint works: Test one loan endpoint
- [ ] Logs configured and readable
- [ ] Backup strategy in place
- [ ] Firewall rules allow port 5000

---

## 🎯 Next Steps

1. **Choose deployment option** (A, B, C, or D above)
2. **Configure environment variables** (copy and edit `.env`)
3. **Run deployment** (follow steps for your chosen option)
4. **Verify** using health check endpoints
5. **Monitor** - Watch logs in production
6. **Backup** - Set up regular database backups

---

## 📞 Support

- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive guide
- Check [DEPLOYMENT_FIX.md](./DEPLOYMENT_FIX.md) for GitHub error fixes
- Review logs: `docker logs biller` or `/var/log/biller/error.log`
- Test endpoints with demo: `python demo_api.py`

---

**Status**: ✅ Your application is ready to deploy!

Deploy now with: `docker-compose up -d` (Option C - recommended)
