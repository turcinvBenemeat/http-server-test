# Caddy Setup Guide for HTTPS

Caddy is the easiest way to set up HTTPS - it automatically handles SSL certificates with Let's Encrypt!

## Why Caddy?

- ✅ **Automatic HTTPS** - Gets SSL certificates automatically
- ✅ **Auto-renewal** - Certificates renew automatically
- ✅ **Simple configuration** - Much easier than Nginx
- ✅ **Perfect for Gmail** - Provides HTTPS needed for images

## Installation

### Ubuntu/Debian

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

### CentOS/RHEL

```bash
dnf install 'dnf-command(copr)'
dnf copr enable @caddy/caddy
dnf install caddy
```

### macOS

```bash
brew install caddy
```

### Docker (Alternative)

```bash
docker pull caddy:latest
```

## Configuration

### Step 1: Copy Caddyfile

```bash
sudo cp config/Caddyfile /etc/caddy/Caddyfile
```

### Step 2: Edit Caddyfile

```bash
sudo nano /etc/caddy/Caddyfile
```

Replace `your-domain.com` with your actual domain name.

**If you have a domain:**
```
your-domain.com {
    reverse_proxy localhost:3000
}
```

**If you only have an IP address:**
```
your-public-ip {
    reverse_proxy localhost:3000
    tls internal
}
```

### Step 3: Start Caddy

```bash
# Check configuration
sudo caddy validate --config /etc/caddy/Caddyfile

# Start Caddy service
sudo systemctl start caddy
sudo systemctl enable caddy

# Check status
sudo systemctl status caddy
```

### Step 4: Update Firewall

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## Docker Setup (Alternative)

If you prefer Docker:

```bash
docker run -d \
  --name caddy \
  -p 80:80 -p 443:443 \
  -v /etc/caddy/Caddyfile:/etc/caddy/Caddyfile \
  -v caddy_data:/data \
  -v caddy_config:/config \
  caddy:latest
```

## Domain Setup

**👉 Don't have a domain? See [FREE_DOMAIN_SETUP.md](FREE_DOMAIN_SETUP.md) for free options!**

### Option 1: Use Free Domain (Recommended)

- **DuckDNS** (free, easiest): https://www.duckdns.org/
- **No-IP** (free): https://www.noip.com/
- **Freenom** (free .tk/.ml domains): https://www.freenom.com/

See [FREE_DOMAIN_SETUP.md](FREE_DOMAIN_SETUP.md) for detailed instructions.

### Option 2: Use Your Own Domain

1. Point your domain's A record to your server's public IP
2. Update Caddyfile with your domain
3. Caddy will automatically get SSL certificate

### Option 3: Use Public IP (Not Recommended for Gmail)

If you only have a public IP, Caddy can work but with self-signed certificates (browser warnings, may not work in Gmail).

## Testing

After setup:

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

### Check Caddy logs
```bash
sudo journalctl -u caddy -f
```

### Validate configuration
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
```

### Restart Caddy
```bash
sudo systemctl restart caddy
```

### Check if ports are open
```bash
sudo netstat -tlnp | grep -E ':(80|443)'
```

## Quick Setup Script

```bash
#!/bin/bash
# Quick Caddy setup script

# Install Caddy (Ubuntu/Debian)
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Copy Caddyfile
sudo cp config/Caddyfile /etc/caddy/Caddyfile

# Edit domain (you need to do this manually)
echo "Edit /etc/caddy/Caddyfile and replace 'your-domain.com' with your domain"

# Start Caddy
sudo systemctl start caddy
sudo systemctl enable caddy

# Open firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

echo "Caddy is now running! Edit /etc/caddy/Caddyfile with your domain."
```

## Advantages of Caddy

- **Zero-config HTTPS** - Automatic SSL certificates
- **Auto-renewal** - Never worry about expiring certificates
- **Simple syntax** - Much easier than Nginx
- **Built-in security** - Good defaults out of the box

## Next Steps

1. Install Caddy
2. Configure Caddyfile with your domain
3. Start Caddy service
4. Test HTTPS access
5. Use HTTPS URL in Gmail!

