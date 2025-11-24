#!/bin/bash
# Deployment script for HTTP server
# Usage: ./deploy.sh [server_user@server_host] [deploy_path]

set -e

SERVER="${1:-deploy@your-server.com}"
DEPLOY_PATH="${2:-/opt/http-server-test}"
APP_NAME="http-server-test"

echo "🚀 Deploying to ${SERVER}..."

# Copy files to server
echo "📦 Copying files to server..."
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' \
    --exclude '.env' --exclude 'venv' --exclude '.venv' \
    ./ ${SERVER}:${DEPLOY_PATH}/

# Deploy on server
echo "🔧 Deploying on server..."
ssh ${SERVER} << EOF
    set -e
    cd ${DEPLOY_PATH}
    
    echo "📥 Pulling latest Docker image..."
    docker-compose pull || docker-compose build
    
    echo "🛑 Stopping existing containers..."
    docker-compose down || true
    
    echo "▶️  Starting new containers..."
    docker-compose up -d
    
    echo "⏳ Waiting for service to be healthy..."
    sleep 5
    
    echo "🏥 Checking health..."
    docker-compose ps
    
    echo "✅ Deployment complete!"
EOF

echo "🎉 Deployment finished successfully!"

