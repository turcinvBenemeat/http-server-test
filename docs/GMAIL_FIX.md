# Fix Gmail Image Access

## Problem
Gmail shows: "We can't find or access the image at that URL"

**Why:**
- ❌ Using HTTP instead of HTTPS
- ❌ Using private IP (10.245.10.20) - Gmail blocks these
- ✅ Need: HTTPS + Public domain/IP

## Solution: Get Free Domain (5 minutes)

### Step 1: Sign up for DuckDNS (Free)

1. Go to https://www.duckdns.org/
2. Sign in with Google/GitHub
3. Create subdomain (e.g., `myserver.duckdns.org`)
4. Add your public IP: `93.90.162.141`
5. Click "Update IP"

### Step 2: Update Caddy Configuration

The Caddyfile is embedded in `docker-compose.yml`. Update it to use your domain:

```bash
# Edit docker-compose.yml
nano docker-compose.yml
```

Find the Caddy command and replace with your domain:

```yaml
command: ["sh", "-c", "rm -rf /etc/caddy/Caddyfile && cat > /etc/caddy/Caddyfile << 'CADDYEOF'
your-domain.duckdns.org {
    reverse_proxy http-server:3000
    encode gzip zstd
    header {
        X-Content-Type-Options \"nosniff\"
        X-Frame-Options \"DENY\"
        X-XSS-Protection \"1; mode=block\"
        Strict-Transport-Security \"max-age=31536000; includeSubDomains\"
        Referrer-Policy \"strict-origin-when-cross-origin\"
    }
}
CADDYEOF
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"]
```

Replace `your-domain.duckdns.org` with your actual DuckDNS domain.

### Step 3: Configure Gateway Router

Since your server is behind a gateway (`10.245.10.254`), you need to configure it:

**Option A: Configure Gateway Nginx (if you have access)**

SSH into gateway and add:

```nginx
server {
    listen 80;
    server_name your-domain.duckdns.org;
    
    location / {
        proxy_pass http://10.245.10.20:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Option B: Port Forwarding**

Configure router to forward:
- Port 80 → 10.245.10.20:80
- Port 443 → 10.245.10.20:443

### Step 4: Deploy

```bash
git add docker-compose.yml
git commit -m "Add domain configuration for Gmail"
git push origin main

# Jenkins will auto-deploy, or manually:
docker-compose up -d --build
```

### Step 5: Use in Gmail

After deployment (wait 2-3 minutes for DNS/SSL):

1. **Image URL:**
   ```
   https://your-domain.duckdns.org/resources/logo.png
   ```

2. **Or copy from webpage:**
   - Open: `https://your-domain.duckdns.org`
   - Click "Copy Logo" button
   - Paste in Gmail

## Quick Test

```bash
# Test HTTPS
curl -k https://your-domain.duckdns.org/health

# Test image
curl -I https://your-domain.duckdns.org/resources/logo.png
```

## Troubleshooting

**DNS not resolving?**
- Wait 5-10 minutes for DNS propagation
- Check: `nslookup your-domain.duckdns.org`

**SSL certificate not working?**
- Make sure port 80 is accessible (needed for Let's Encrypt)
- Check Caddy logs: `docker logs caddy-proxy`

**Still can't access externally?**
- Configure gateway/router to forward ports
- Or configure gateway's nginx to proxy

