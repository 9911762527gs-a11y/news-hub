#!/bin/bash

# News Hub Start Script for Railway
# This script is called when the container starts

set -e

echo "=========================================="
echo "News Hub - Railway Start Script"
echo "=========================================="
echo "Starting at: $(date)"
echo ""

# Create necessary directories
mkdir -p /app/output
mkdir -p /app/logs
mkdir -p /app/assets/backgrounds
mkdir -p /app/assets/characters
mkdir -p /app/assets/fonts

echo "✓ Directories created"

# Check if this is the scheduler service
if [ "$RAILWAY_SERVICE" = "scheduler" ]; then
    echo "Starting SCHEDULER service..."
    echo ""
    exec python -m news_hub.scheduler

# Check if this is the API/dashboard service
elif [ "$RAILWAY_SERVICE" = "api" ]; then
    echo "Starting API/DASHBOARD service..."
    echo ""
    exec python deploy/dashboard.py

# Default: run scheduler
else
    echo "Starting DEFAULT service (scheduler)..."
    echo ""
    exec python -m news_hub.scheduler
fi
