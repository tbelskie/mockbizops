#!/bin/bash

# Car Repair Shop API - Run Script

set -e

echo "========================================"
echo "Car Repair Shop Mock API"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your database credentials"
    exit 1
fi

# Check database connection
echo "Checking database connection..."
python -c "from app.database import engine; engine.connect()" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Database connection failed!"
    echo "Please check your DATABASE_URL in .env file"
    exit 1
fi

echo "✓ Database connection successful"

# Check if database has data
echo "Checking if database is seeded..."
CUSTOMER_COUNT=$(python -c "from app.database import SessionLocal; from app.models import Customer; db = SessionLocal(); print(db.query(Customer).count()); db.close()" 2>/dev/null)

if [ "$CUSTOMER_COUNT" = "0" ]; then
    echo ""
    echo "Database is empty. Would you like to seed it with mock data? (y/n)"
    read -r response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        echo "Seeding database..."
        python -m app.seed_data
    fi
fi

echo ""
echo "========================================"
echo "Starting API server..."
echo "========================================"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
