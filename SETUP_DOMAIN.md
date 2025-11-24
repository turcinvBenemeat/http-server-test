# Quick Setup: Get Domain for Gmail

## Step 1: Get Free DuckDNS Domain (2 minutes)

1. Go to **https://www.duckdns.org/**
2. Sign in with **Google** or **GitHub**
3. Create subdomain (e.g., `myserver`)
4. Your domain will be: `myserver.duckdns.org`
5. Add IP: `93.90.162.141`
6. Click **"Update IP"**

## Step 2: Update docker-compose.yml

After you have your domain, edit `docker-compose.yml`:

1. Find the Caddy command (around line 34)
2. Find this line: `# YOUR-DOMAIN.duckdns.org {`
3. Uncomment it and replace `YOUR-DOMAIN.duckdns.org` with your actual domain
4. Example: `myserver.duckdns.org {`

**Before:**
```yaml
# YOUR-DOMAIN.duckdns.org {
```

**After:**
```yaml
myserver.duckdns.org {
```

## Step 3: Configure Gateway Router

Your server is behind gateway `10.245.10.254`. You need to configure it:

**Option A: Configure Gateway Nginx (if you have SSH access)**

SSH into the gateway and create `/etc/nginx/sites-available/your-domain`:

```nginx
server {
    listen 80;
    server_name myserver.duckdns.org;
    
    location / {
        proxy_pass http://10.245.10.20:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then:
```bash
sudo ln -s /etc/nginx/sites-available/your-domain /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Option B: Port Forwarding**

Configure router to forward:
- Port 80 → 10.245.10.20:80
- Port 443 → 10.245.10.20:443

## Step 4: Deploy

```bash
git add docker-compose.yml
git commit -m "Configure domain for Gmail"
git push origin main
```

Jenkins will auto-deploy. Wait 2-3 minutes for DNS and SSL certificate.

## Step 5: Use in Gmail

After deployment:

1. **Image URL:**
   ```
   https://myserver.duckdns.org/resources/logo.png
   ```

2. **Or copy from webpage:**
   - Open: `https://myserver.duckdns.org`
   - Click "Copy Logo" button
   - Paste in Gmail ✅

## Test

```bash
# Test HTTPS
curl -k https://myserver.duckdns.org/health

# Test image
curl -I https://myserver.duckdns.org/resources/logo.png
```

