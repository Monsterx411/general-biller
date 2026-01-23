#!/bin/bash
# Deploy script for globe-swift.org

set -e

echo "🚀 Deploying General Biller to globe-swift.org..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Copy .env.example to .env and set values."
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
