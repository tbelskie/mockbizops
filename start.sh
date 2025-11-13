#!/bin/bash
# Startup script for Railway/Render deployment

# Use PORT environment variable if set, otherwise default to 8000
PORT=${PORT:-8000}

echo "Starting application on port $PORT"

# Start uvicorn with the PORT
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
