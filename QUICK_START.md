# Quick Start Deployment Guide

## 🚀 Quick Deploy to Your Server

### Option 1: Manual Deployment (Fastest)

**On your server:**
```bash
# 1. Clone the repository
git clone https://github.com/your-username/http-server-test.git
cd http-server-test

# 2. Deploy
docker-compose up -d --build

# 3. Check status
docker-compose ps
curl http://localhost:3000/health
```

### Option 2: Using Deployment Script

**From your local machine:**
```bash
# Edit deploy.sh and set your server details, then:
./deploy.sh user@your-server.com /opt/http-server-test
```

**On your server:**
```bash
cd /opt/http-server-test
./deploy-manual.sh
```

### Option 3: Jenkins Automated Deployment

1. **Configure Jenkins:**
   - Add SSH credentials (ID: `ssh-deploy-key`)
   - Set environment variables:
     - `DEPLOY_SERVER`: `user@your-server.com`
     - `DEPLOY_PATH`: `/opt/http-server-test`
     - `DEPLOY_SSH_CREDENTIALS`: `ssh-deploy-key`
     - `DEPLOY_URL`: `http://your-server.com:3000`

2. **Prepare server (first time only):**
   ```bash
   ssh user@your-server.com
   sudo mkdir -p /opt/http-server-test
   sudo chown $USER:$USER /opt/http-server-test
   cd /opt/http-server-test
   git clone https://github.com/your-username/http-server-test.git .
   ```

3. **Run Jenkins pipeline** - it will automatically deploy!

## 📋 Prerequisites

- Server with SSH access
- Docker and Docker Compose installed
- Port 3000 open (or change in docker-compose.yml)

## ✅ Verify Deployment

```bash
# Check container
docker-compose ps

# Check health
curl http://localhost:3000/health

# View logs
docker-compose logs -f

# Access API docs
# http://your-server:3000/docs
```

## 🔧 Troubleshooting

- **Port in use?** Change port in `docker-compose.yml`
- **Permission denied?** Add user to docker group: `sudo usermod -aG docker $USER`
- **Container won't start?** Check logs: `docker-compose logs`

For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

