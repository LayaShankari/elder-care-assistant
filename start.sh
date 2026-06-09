#!/bin/bash
# Quick Start Script for Elder Care Assistant

set -e

echo "🚀 Elder Care Assistant - Quick Start"
echo "====================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.10 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy .env if not exists
if [ ! -f ".env" ]; then
    echo "📋 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Start services
echo ""
echo "🔧 Starting services..."
echo ""
echo "Services to start (in separate terminals):"
echo "1. Redis:    redis-server"
echo "2. Celery:   celery -A app.tasks.celery worker --loglevel=info"
echo "3. API:      uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Or use Docker Compose:"
echo "docker-compose up -d"
echo ""
echo "✅ Ready! API will be available at http://localhost:8000"
echo "📚 API Docs at http://localhost:8000/docs"
