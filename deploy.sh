#!/bin/bash

set -e  # Exit on any error

echo "Deploying Automation Dashboard..."

# Deploy infrastructure
echo "Installing infrastructure dependencies..."
cd infrastructure
npm install || { echo "Failed to install infrastructure dependencies"; exit 1; }

echo "Deploying AWS infrastructure..."
npx cdk deploy || { echo "Failed to deploy infrastructure"; exit 1; }

# Deploy backend
echo "Installing backend dependencies..."
cd ../backend
pip install -r requirements.txt || { echo "Failed to install backend dependencies"; exit 1; }

echo "Starting backend server..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Build and serve frontend
echo "Installing frontend dependencies..."
cd ../frontend
npm install || { echo "Failed to install frontend dependencies"; kill $BACKEND_PID; exit 1; }

echo "Building frontend..."
npm run build || { echo "Failed to build frontend"; kill $BACKEND_PID; exit 1; }

echo "Starting frontend server..."
npx serve -s build -l 3000 &
FRONTEND_PID=$!

echo "Deployment complete!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "Press Ctrl+C to stop all services"

# Wait for interrupt signal
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait