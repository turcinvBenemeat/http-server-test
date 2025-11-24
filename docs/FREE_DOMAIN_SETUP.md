# Free Domain Setup Guide

Don't have a domain? No problem! Here are free options to get HTTPS working for Gmail.

## Why You Need a Domain for Gmail

- Gmail requires **HTTPS** (not HTTP)
- Gmail blocks **private IPs** (192.168.x.x, 10.x.x.x)
- Gmail blocks **self-signed certificates** (browser warnings)
- **Solution:** Use a free domain with Let's Encrypt SSL

## Option 1: DuckDNS (Recommended - Easiest)

### Step 1: Sign Up
1. Go to https://www.duckdns.org/
2. Sign in with Google/GitHub (free)
3. Create a subdomain (e.g., `my-server.duckdns.org`)

### Step 2: Update DNS
1. In DuckDNS, add your public IP address
2. Click "Update IP"
3. Wait a few minutes for DNS propagation

### Step 3: Update Caddyfile
```bash
nano config/Caddyfile
```

Replace with:
```
my-server.duckdns.org {
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

### Step 4: Deploy
```bash
docker-compose up -d
```

Caddy will automatically get SSL certificate!

## Option 2: No-IP (Free Dynamic DNS)

### Step 1: Sign Up
1. Go to https://www.noip.com/
2. Create free account
3. Create hostname (e.g., `my-server.ddns.net`)

### Step 2: Install No-IP Client (Optional)
- Or manually update IP in web interface
- Or use their API

### Step 3: Update Caddyfile
Same as DuckDNS, but use your No-IP hostname.

## Option 3: Freenom (Free .tk/.ml/.ga Domains)

### Step 1: Sign Up
1. Go to https://www.freenom.com/
2. Search for free domain (.tk, .ml, .ga, .cf, .gq)
3. Register domain (free for 1 year)

### Step 2: Configure DNS
1. Point A record to your public IP
2. Wait for DNS propagation

### Step 3: Update Caddyfile
Use your Freenom domain name.

## Option 4: Cloudflare Tunnel (No Port Forwarding!)

If you can't open ports 80/443:

1. Sign up for Cloudflare (free)
2. Install `cloudflared` tunnel
3. No port forwarding needed!
4. Get HTTPS automatically

## Quick Setup with DuckDNS

```bash
# 1. Get your public IP
curl ifconfig.me

# 2. Sign up at duckdns.org and add IP

# 3. Update Caddyfile
nano config/Caddyfile
# Change to: yourname.duckdns.org

# 4. Deploy
docker-compose up -d

# 5. Access!
https://yourname.duckdns.org
```

## Testing

After setup:

```bash
# Test HTTPS
curl https://your-domain.duckdns.org/health

# Test in browser
https://your-domain.duckdns.org

# Test logo URL for Gmail
https://your-domain.duckdns.org/resources/logo.png
```

## Troubleshooting

### DNS not resolving?
- Wait 5-10 minutes for propagation
- Check DNS: `nslookup your-domain.duckdns.org`
- Verify IP is correct in DuckDNS

### SSL certificate not working?
- Make sure port 80 is open (for Let's Encrypt verification)
- Check Caddy logs: `docker-compose logs caddy`
- Verify domain points to your IP

### Still not working?
- Check firewall: `sudo ufw allow 80/tcp && sudo ufw allow 443/tcp`
- Check Caddyfile syntax: `docker-compose exec caddy caddy validate --config /etc/caddy/Caddyfile`

## Recommendation

**Use DuckDNS** - It's the easiest and most reliable free option!

1. Free forever
2. Easy setup (5 minutes)
3. Works perfectly with Caddy
4. Automatic SSL certificates
5. Perfect for Gmail!

