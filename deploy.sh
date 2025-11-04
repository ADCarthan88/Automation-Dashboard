#!/bin/bash

echo "Deploying Automation Dashboard..."

# Deploy infrastructure
cd infrastructure
npm install
npx cdk deploy

# Deploy backend
cd ../backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Build and serve frontend
cd ../frontend
npm install
npm run build
npx serve -s build -l 3000

echo "Deployment complete!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"