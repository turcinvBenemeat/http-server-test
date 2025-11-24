# Quick Connection Guide

Step-by-step guide to get your server running and accessible.

## Prerequisites Checklist

- [ ] Server with Docker installed
- [ ] Public IP address (or domain name)
- [ ] Ports 80 and 443 open in firewall
- [ ] Jenkins server configured (for auto-deployment)

## Step 1: Get Your Public IP Address

On your server, run:
```bash
curl ifconfig.me
# or
curl ipinfo.io/ip
```

**Save this IP address** - you'll need it!

## Step 2: Choose Your Setup Method

### Option A: Free Domain (Recommended for Gmail) ⭐

**Best for:** Using logo in Gmail (requires HTTPS)

1. **Sign up for DuckDNS** (free, 2 minutes):
   - Go to https://www.duckdns.org/
   - Sign in with Google/GitHub
   - Create subdomain (e.g., `myserver.duckdns.org`)
   - Add your public IP address
   - Click "Update IP"

2. **Update Caddyfile**:
   ```bash
   nano config/Caddyfile
   ```
   
   Uncomment and edit:
   ```caddy
   myserver.duckdns.org {
       reverse_proxy http-server:3000
       encode gzip zstd
       header {
           Strict-Transport-Security "max-age=31536000; includeSubDomains"
           X-Content-Type-Options "nosniff"
           X-Frame-Options "DENY"
           X-XSS-Protection "1; mode=block"
           Referrer-Policy "strict-origin-when-cross-origin"
       }
   }
   ```

3. **Open firewall ports**:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

4. **Deploy**:
   ```bash
   docker-compose up -d --build
   ```

5. **Access**:
   - Webpage: `https://myserver.duckdns.org`
   - Logo: `https://myserver.duckdns.org/resources/logo.png` ✅ Works in Gmail!

### Option B: IP Address Only (Quick Test)

**Best for:** Quick testing (may not work in Gmail)

1. **Update Caddyfile**:
   ```bash
   nano config/Caddyfile
   ```
   
   Make sure this is active:
   ```caddy
   :443 {
       reverse_proxy http-server:3000
       tls internal
       encode gzip zstd
   }
   ```

2. **Open firewall ports**:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

3. **Deploy**:
   ```bash
   docker-compose up -d --build
   ```

4. **Access**:
   - HTTPS: `https://YOUR_PUBLIC_IP` (browser warning, but works)
   - HTTP: `http://YOUR_PUBLIC_IP:3000` (direct FastAPI)

## Step 3: Verify Everything Works

### Check Containers
```bash
docker-compose ps
```

Should show:
- `http-server-test` - Running
- `caddy-proxy` - Running

### Check Logs
```bash
# FastAPI logs
docker-compose logs http-server

# Caddy logs
docker-compose logs caddy
```

### Test Endpoints
```bash
# Health check
curl http://localhost:3000/health

# If using domain
curl https://your-domain.com/health

# If using IP
curl -k https://YOUR_PUBLIC_IP/health
```

## Step 4: Access Your Webpage

### From Browser
- **With domain**: `https://your-domain.com`
- **With IP**: `https://YOUR_PUBLIC_IP` (accept security warning)

### From Another Computer
- Use the same URLs as above
- Make sure firewall allows connections

## Step 5: Use Logo in Gmail

### Method 1: Direct URL (Easiest)
1. Get your logo URL:
   - With domain: `https://your-domain.com/resources/logo.png`
   - With IP: `https://YOUR_PUBLIC_IP/resources/logo.png`

2. In Gmail:
   - Click "Insert photo"
   - Paste the URL
   - Image appears! ✅

### Method 2: Copy from Webpage
1. Open your webpage: `https://your-domain.com`
2. Click "Copy Logo" button
3. Paste in Gmail (Ctrl+V / Cmd+V)

## Troubleshooting

### Can't access from outside?
```bash
# Check if containers are running
docker-compose ps

# Check if ports are open
sudo netstat -tlnp | grep -E ':(80|443|3000)'

# Check firewall
sudo ufw status
```

### Caddy not getting SSL certificate?
```bash
# Check Caddy logs
docker-compose logs caddy

# Verify domain points to your IP
nslookup your-domain.com

# Make sure port 80 is open (needed for Let's Encrypt)
sudo ufw allow 80/tcp
```

### Logo not showing in Gmail?
- ✅ Must use HTTPS (not HTTP)
- ✅ Must use public domain/IP (not localhost)
- ✅ Domain must have valid SSL certificate
- ❌ Self-signed certificates may not work

## Quick Commands Reference

```bash
# Start everything
docker-compose up -d --build

# Stop everything
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Update and redeploy
git pull
docker-compose up -d --build
```

## Next Steps

1. ✅ Get public IP or free domain
2. ✅ Update Caddyfile
3. ✅ Open firewall ports
4. ✅ Deploy with docker-compose
5. ✅ Test access
6. ✅ Use logo URL in Gmail!

## Need Help?

- See `docs/FREE_DOMAIN_SETUP.md` for domain setup
- See `docs/CADDY_SETUP.md` for Caddy details
- Check logs: `docker-compose logs`

