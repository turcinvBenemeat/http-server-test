# Router/Gateway Setup Guide

## Problem

You're behind a router/gateway (`10.245.10.254`) with NAT. Both your server and computer share the same public IP (`93.90.162.141`). The gateway's Nginx is intercepting requests, blocking access to your server.

## Solution: Configure Port Forwarding

You need to forward ports from the router to your server.

### Step 1: Access Router/Gateway

1. **Find router IP:** `10.245.10.254` (your gateway)
2. **Access router admin:**
   - Open browser: `http://10.245.10.254` or `https://10.245.10.254`
   - Or SSH: `ssh admin@10.245.10.254` (if you have access)

### Step 2: Configure Port Forwarding

In router admin panel, set up port forwarding:

**Forward these ports:**
- **Port 80** (HTTP) → `10.245.10.20:80`
- **Port 443** (HTTPS) → `10.245.10.20:443`

**Common router settings location:**
- "Port Forwarding" or "Virtual Server"
- "NAT" → "Port Forwarding"
- "Firewall" → "Port Forwarding"

**Example configuration:**
```
Service Name: HTTP Server
External Port: 80
Internal IP: 10.245.10.20
Internal Port: 80
Protocol: TCP

Service Name: HTTPS Server
External Port: 443
Internal IP: 10.245.10.20
Internal Port: 443
Protocol: TCP
```

### Step 3: Disable Gateway Nginx (if possible)

If you have SSH access to the gateway:

```bash
ssh admin@10.245.10.254
sudo systemctl stop nginx
sudo systemctl disable nginx
```

**OR** configure gateway Nginx to proxy to your server (see Option B below).

### Step 4: Test

After port forwarding:

```bash
# From your server
curl http://93.90.162.141/health

# Should work now!
```

---

## Alternative: Configure Gateway Nginx

If you can't do port forwarding, configure the gateway Nginx to proxy requests:

### SSH into Gateway

```bash
ssh admin@10.245.10.254
```

### Create Nginx Config

```bash
sudo nano /etc/nginx/sites-available/http-server
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name 93.90.162.141;  # Public IP
    
    location / {
        proxy_pass http://10.245.10.20:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl;
    server_name 93.90.162.141;  # Public IP
    
    # SSL certificates (if you have them)
    # ssl_certificate /path/to/cert.pem;
    # ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://10.245.10.20:443;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable and Reload

```bash
sudo ln -s /etc/nginx/sites-available/http-server /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## After Router Setup: Get DuckDNS Domain

Once port forwarding works:

1. **Get free domain:** https://www.duckdns.org/
2. **Set IP:** `93.90.162.141`
3. **Tell me your domain** and I'll configure Caddy automatically!

---

## Quick Test Commands

```bash
# Test from server
curl http://93.90.162.141/health

# Test from external computer
curl http://93.90.162.141/health

# Check if port forwarding is working
# (should see your server's response, not gateway Nginx 404)
```

---

## Still Not Working?

1. **Check firewall on router:**
   - Ensure ports 80/443 are open in firewall rules

2. **Check server firewall:**
   ```bash
   sudo ufw status
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

3. **Verify Docker ports:**
   ```bash
   docker ps | grep caddy
   # Should show: 0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
   ```

4. **Test locally first:**
   ```bash
   curl http://10.245.10.20/health  # Should work
   curl http://localhost/health     # Should work
   ```

