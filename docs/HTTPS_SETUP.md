# HTTPS Setup Guide for Gmail Compatibility

Gmail requires **HTTPS** and a **public IP/domain** to display images. This guide shows how to set up HTTPS for your server.

**👉 For easiest setup, see [CADDY_SETUP.md](CADDY_SETUP.md) - Caddy automatically handles HTTPS!**

## Why HTTPS is Needed

- ✅ Gmail blocks HTTP images for security
- ✅ Gmail blocks local/private IP addresses (192.168.x.x, 10.x.x.x, etc.)
- ✅ HTTPS ensures secure image delivery
- ✅ Public domain/IP allows external access

## Option 1: Using Nginx Reverse Proxy (Recommended)

### Step 1: Install Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

### Step 2: Install Certbot (Let's Encrypt SSL)

```bash
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

### Step 3: Get SSL Certificate

**If you have a domain name:**
```bash
sudo certbot --nginx -d your-domain.com
```

**If you only have a public IP:**
You'll need a domain name. Consider using:
- Free domains: Freenom, DuckDNS
- Or use your server provider's domain service

### Step 4: Configure Nginx

1. Copy the config file:
```bash
sudo cp config/nginx.conf /etc/nginx/sites-available/http-server-test
```

2. Edit the file:
```bash
sudo nano /etc/nginx/sites-available/http-server-test
```

3. Replace `your-domain.com` with your actual domain/IP

4. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/http-server-test /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

### Step 5: Update Firewall

```bash
# Allow HTTPS (port 443)
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp  # For Let's Encrypt verification
```

## Option 2: Direct HTTPS with Uvicorn (Simpler, but less secure)

### Step 1: Generate Self-Signed Certificate (for testing)

```bash
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=your-domain.com"
```

### Step 2: Update Dockerfile

Add certificate files and update CMD:
```dockerfile
COPY cert.pem key.pem ./
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "3000", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]
```

**Note:** Self-signed certificates will show a warning in browsers. Use Let's Encrypt for production.

## Option 3: Use Cloudflare (Easiest)

1. Sign up for Cloudflare (free)
2. Add your domain
3. Enable "Always Use HTTPS"
4. Cloudflare provides free SSL automatically

## Testing

After setup, test your HTTPS:

```bash
# Test HTTPS endpoint
curl https://your-domain.com/health

# Test in browser
https://your-domain.com
```

## For Gmail

Once HTTPS is set up:

1. **Direct image URL:**
   ```
   https://your-domain.com/resources/logo.png
   ```
   Paste this URL in Gmail - it will display the image.

2. **Or use the webpage:**
   ```
   https://your-domain.com
   ```
   Copy the logo from the webpage and paste into Gmail.

## Troubleshooting

### Certificate errors
- Make sure domain points to your server IP
- Check firewall allows port 443
- Verify certificate files exist

### Images not loading in Gmail
- Must use HTTPS (not HTTP)
- Must use public domain/IP (not localhost or private IP)
- Check CORS headers if needed

### Nginx not starting
```bash
sudo nginx -t  # Check configuration
sudo systemctl status nginx  # Check status
sudo journalctl -u nginx  # Check logs
```

## Quick Checklist

- [ ] Domain name or public IP configured
- [ ] Nginx installed
- [ ] SSL certificate obtained (Let's Encrypt)
- [ ] Nginx configured and running
- [ ] Port 443 open in firewall
- [ ] FastAPI app running on port 3000
- [ ] Test HTTPS access works
- [ ] Test image URL in Gmail

