# Deployment Guide

This guide covers different methods to deploy the HTTP server to your server.

## Prerequisites

- Server with SSH access
- Docker and Docker Compose installed on the server
- Jenkins server (for automated deployment)

## Method 1: Automated Deployment via Jenkins (Recommended)

### Step 1: Prepare Your Server

1. **SSH into your server:**
   ```bash
   ssh user@your-server.com
   ```

2. **Create deployment directory:**
   ```bash
   sudo mkdir -p /opt/http-server-test
   sudo chown $USER:$USER /opt/http-server-test
   cd /opt/http-server-test
   ```

3. **Clone the repository (first time only):**
   ```bash
   git clone https://github.com/your-username/http-server-test.git .
   ```

4. **Ensure Docker and Docker Compose are installed:**
   ```bash
   docker --version
   docker-compose --version
   ```

### Step 2: Configure Jenkins

1. **Add SSH Credentials in Jenkins:**
   - Go to: Jenkins → Manage Jenkins → Credentials
   - Click "Add Credentials"
   - Kind: SSH Username with private key
   - ID: `ssh-deploy-key` (or your preferred ID)
   - Username: Your server username
   - Private Key: Enter directly or use a file
   - Description: "SSH key for server deployment"

2. **Configure Jenkins Pipeline:**
   - Open your Jenkins job
   - Go to "Configure"
   - Under "Build Environment" or in the Jenkinsfile, set:
     - `DEPLOY_SERVER`: `user@your-server.com`
     - `DEPLOY_PATH`: `/opt/http-server-test`
     - `DEPLOY_SSH_CREDENTIALS`: `ssh-deploy-key` (or your credential ID)
     - `DEPLOY_URL`: `http://your-server.com:3000` (or your domain)

3. **Update Jenkinsfile Environment Variables:**
   ```groovy
   environment {
       DEPLOY_SERVER = 'user@your-server.com'
       DEPLOY_PATH = '/opt/http-server-test'
       DEPLOY_SSH_CREDENTIALS = 'ssh-deploy-key'
       DEPLOY_URL = 'http://your-server.com:3000'
   }
   ```

### Step 3: Run Jenkins Pipeline

1. Click "Build Now" in Jenkins
2. The pipeline will:
   - Checkout code
   - Run tests
   - Build Docker image
   - Deploy to your server via SSH
   - Perform health check

## Method 2: Manual Deployment Script

### On Your Local Machine

1. **Make the script executable:**
   ```bash
   chmod +x deploy.sh
   ```

2. **Deploy:**
   ```bash
   ./deploy.sh user@your-server.com /opt/http-server-test
   ```

   Or use defaults:
   ```bash
   # Edit deploy.sh to set your server details, then:
   ./deploy.sh
   ```

### On Your Server

1. **SSH into your server:**
   ```bash
   ssh user@your-server.com
   ```

2. **Navigate to deployment directory:**
   ```bash
   cd /opt/http-server-test
   ```

3. **Run manual deployment script:**
   ```bash
   chmod +x deploy-manual.sh
   ./deploy-manual.sh
   ```

## Method 3: Direct Docker Compose Deployment

### On Your Server

1. **SSH into your server:**
   ```bash
   ssh user@your-server.com
   ```

2. **Clone or update repository:**
   ```bash
   cd /opt/http-server-test
   git pull origin main  # or clone if first time
   ```

3. **Deploy:**
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

4. **Check status:**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

## Method 4: Direct Docker (without Compose)

### On Your Server

```bash
# Build the image
docker build -t http-server-test .

# Stop and remove old container
docker stop http-server-test || true
docker rm http-server-test || true

# Run new container
docker run -d \
  --name http-server-test \
  -p 3000:3000 \
  --restart unless-stopped \
  http-server-test

# Check logs
docker logs -f http-server-test
```

## Post-Deployment

### Verify Deployment

1. **Check container status:**
   ```bash
   docker-compose ps
   # or
   docker ps
   ```

2. **Check health endpoint:**
   ```bash
   curl http://localhost:3000/health
   # or from outside:
   curl http://your-server-ip:3000/health
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   # or
   docker logs -f http-server-test
   ```

### Access the API

- **API Documentation:** http://your-server:3000/docs
- **Health Check:** http://your-server:3000/health
- **API Endpoints:** http://your-server:3000/api

### Firewall Configuration

If your server has a firewall, open port 3000:

```bash
# UFW (Ubuntu)
sudo ufw allow 3000/tcp

# Firewalld (CentOS/RHEL)
sudo firewall-cmd --add-port=3000/tcp --permanent
sudo firewall-cmd --reload

# iptables
sudo iptables -A INPUT -p tcp --dport 3000 -j ACCEPT
```

### Reverse Proxy (Optional)

For production, consider using Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs
docker-compose ps
```

### Port already in use
```bash
# Find what's using port 3000
sudo lsof -i :3000
# Or change port in docker-compose.yml
```

### Permission denied
```bash
# Ensure user is in docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### Health check fails
```bash
# Check if container is running
docker ps
# Check logs
docker logs http-server-test
# Test manually
curl http://localhost:3000/health
```

## Updating the Deployment

### Via Jenkins
Just push to your repository and Jenkins will automatically deploy.

### Manually
```bash
cd /opt/http-server-test
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

## Rollback

If something goes wrong:

```bash
# Stop current version
docker-compose down

# Use previous image (if tagged)
docker run -d --name http-server-test \
  -p 3000:3000 \
  http-server-test:previous-tag
```

## Monitoring

Consider setting up:
- Log aggregation (ELK, Loki)
- Monitoring (Prometheus, Grafana)
- Uptime monitoring (UptimeRobot, Pingdom)

