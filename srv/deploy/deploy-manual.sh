#!/bin/bash
# Manual deployment script - run this on your server
# Usage: ./deploy-manual.sh

set -e

echo "🚀 Starting manual deployment..."

# Navigate to deployment directory
cd "$(dirname "$0")"

echo "📥 Pulling latest code from Git..."
git pull origin main || echo "⚠️  Git pull failed, continuing with local files..."

echo "🔨 Building Docker image..."
docker-compose build

echo "🛑 Stopping existing containers..."
docker-compose down || true

echo "▶️  Starting containers..."
docker-compose up -d

echo "⏳ Waiting for service to start..."
sleep 5

echo "🏥 Checking health..."
curl -f http://localhost:3000/health || echo "⚠️  Health check failed, but container may still be starting..."

echo "📊 Container status:"
docker-compose ps

echo "✅ Deployment complete!"
echo "🌐 Server should be available at http://localhost:3000"

