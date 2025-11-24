# Quick Fix: nginx Blocking Port 80

## Problem
nginx is running on port 80 and returning 404, blocking access to your app.

## Quick Solution (Choose One)

### Option 1: Stop nginx and Use Caddy (Recommended)

```bash
# Check if nginx is running as a service
sudo systemctl status nginx

# If service exists, stop it:
sudo systemctl stop nginx
sudo systemctl disable nginx

# If service doesn't exist, find and kill nginx processes:
ps aux | grep nginx
sudo pkill -9 nginx
# Or find the PID and kill it:
sudo kill -9 $(pgrep nginx)

# Check what's using port 80:
sudo ss -tlnp | grep :80

# Restart docker-compose (Caddy will handle port 80)
cd /path/to/http-server-test
docker-compose restart caddy

# Verify
curl http://93.90.162.141/health
```

### Option 2: Configure nginx to Proxy (Keep nginx)

```bash
# Create nginx config
sudo cp config/nginx.conf /etc/nginx/sites-available/http-server
sudo ln -s /etc/nginx/sites-available/http-server /etc/nginx/sites-enabled/http-server
sudo rm /etc/nginx/sites-enabled/default  # Remove default site

# Test and reload
sudo nginx -t
sudo systemctl reload nginx

# Verify
curl http://93.90.162.141/health
```

### Option 3: Use Different Port (Keep both)

Update `docker-compose.yml`:
```yaml
caddy:
  ports:
    - "8080:80"  # Change from 80:80 to 8080:80
```

Then access via: `http://93.90.162.141:8080`

## Check What's Using Port 80

```bash
sudo netstat -tlnp | grep :80
# or
sudo ss -tlnp | grep :80
```

## Verify Your App is Running

```bash
# Check containers
docker ps

# Test locally
curl http://localhost:3000/health

# Test from outside (after fixing nginx)
curl http://93.90.162.141/health
```

