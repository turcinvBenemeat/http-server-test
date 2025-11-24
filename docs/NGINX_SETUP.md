# Nginx Setup Guide

## Problem
If you see `404 Not Found` from nginx when accessing your server, nginx is intercepting requests on port 80.

## Solution: Configure Nginx to Proxy to Your App

### Step 1: Check if nginx is running
```bash
sudo systemctl status nginx
```

### Step 2: Create nginx configuration
```bash
# Copy the nginx config file
sudo cp config/nginx.conf /etc/nginx/sites-available/http-server

# Create symlink to enable it
sudo ln -s /etc/nginx/sites-available/http-server /etc/nginx/sites-enabled/http-server

# Remove default nginx site (optional)
sudo rm /etc/nginx/sites-enabled/default
```

### Step 3: Test and reload nginx
```bash
# Test configuration
sudo nginx -t

# If test passes, reload nginx
sudo systemctl reload nginx
```

### Step 4: Verify it works
```bash
curl http://93.90.162.141/health
curl http://93.90.162.141/
```

## Alternative: Stop Nginx and Use Caddy

If you prefer to use Caddy instead:

```bash
# Stop nginx
sudo systemctl stop nginx
sudo systemctl disable nginx

# Use Caddy (already configured in docker-compose.yml)
docker-compose up -d
```

## Alternative: Use Different Port

If you want to keep nginx and use a different port:

1. Update `docker-compose.yml` to use port 8080:
```yaml
ports:
  - "8080:3000"
```

2. Access via: `http://93.90.162.141:8080`

## Troubleshooting

### Check what's listening on port 80
```bash
sudo netstat -tlnp | grep :80
# or
sudo ss -tlnp | grep :80
```

### Check nginx error logs
```bash
sudo tail -f /var/log/nginx/error.log
```

### Check if your app is running
```bash
docker ps
curl http://localhost:3000/health
```

