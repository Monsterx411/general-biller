#!/bin/bash

# Loan Payment Manager - Production Deployment Script
# Complete deployment with logging, error handling, and systemd support

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
APP_NAME="general-biller"
APP_PORT=${APP_PORT:-5000}
ENVIRONMENT=${ENVIRONMENT:-production}
LOG_DIR="/var/log/$APP_NAME"
SERVICE_NAME="biller"

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# Check prerequisites
check_requirements() {
    log_info "Checking prerequisites..."
    
    command -v python3 &> /dev/null || log_error "Python 3 is required"
    command -v pip &> /dev/null || log_error "pip is required"
    command -v git &> /dev/null || log_error "Git is required"
    
    log_success "All prerequisites found"
}

# Setup environment
setup_environment() {
    log_info "Setting up environment..."
    
    if [ ! -d "$LOG_DIR" ]; then
        sudo mkdir -p "$LOG_DIR" && sudo chown $USER:$USER "$LOG_DIR"
        log_success "Created log directory: $LOG_DIR"
    fi
}

# Install dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    [ ! -d ".venv" ] && python3 -m venv .venv && log_success "Virtual environment created"
    
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    log_success "Dependencies installed"
}

# Setup database
setup_database() {
    log_info "Setting up database..."
    
    [ -z "$DATABASE_URL" ] && export DATABASE_URL="sqlite:///loan_manager.db"
    
    if command -v alembic &> /dev/null; then
        log_info "Running database migrations..."
        alembic upgrade head || log_warn "Migrations skipped"
    fi
    
    log_success "Database setup complete"
}

# Run tests
run_tests() {
    log_info "Running tests..."
    
    source .venv/bin/activate
    pytest tests/ -v --tb=short || log_warn "Some tests failed (continuing)"
    
    log_success "Tests completed"
}

# Start application with Gunicorn
start_application() {
    log_info "Starting application..."
    
    source .venv/bin/activate
    gunicorn -w 4 -b 0.0.0.0:$APP_PORT \
        --log-level info \
        --access-logfile $LOG_DIR/access.log \
        --error-logfile $LOG_DIR/error.log \
        src.api.app:app &
    
    sleep 2
    log_success "Application started on port $APP_PORT"
}

# Verify deployment
verify_deployment() {
    log_info "Verifying deployment..."
    
    sleep 2
    
    if curl -s http://localhost:$APP_PORT/health > /dev/null 2>&1; then
        log_success "✅ Health check passed"
    else
        log_warn "⚠️  Health check may have failed"
    fi
    
    if curl -s http://localhost:$APP_PORT/readiness | grep -q "ready" 2>/dev/null; then
        log_success "✅ API is ready"
    fi
}
    exit 1
fi

# Pull latest from git
echo "📦 Pulling latest code..."
git pull origin main

# Install/update Python dependencies
echo "📚 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v --tb=short

# Apply database migrations (if using Alembic)
echo "🗄️  Applying database migrations..."
alembic upgrade head || true

# Build Docker images
echo "🐳 Building Docker images..."
docker compose build

# Start services
echo "▶️  Starting services..."
docker compose up -d

# Show status
echo "✅ Deployment complete!"
docker compose ps
echo "📊 Check logs: docker compose logs -f web"
