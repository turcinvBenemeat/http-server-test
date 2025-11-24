# Quick Free Domain Setup (2 Minutes)

## Get Free Domain for Gmail

### Step 1: Sign Up (30 seconds)

1. Go to: **https://www.duckdns.org/**
2. Click **"Sign in with Google"** or **"Sign in with GitHub"**
3. Authorize the app

### Step 2: Create Domain (30 seconds)

1. In DuckDNS dashboard, you'll see a text box
2. Type your desired subdomain (e.g., `myserver` or `logo` or `test123`)
3. Click **"Add Domain"**
4. Your domain will be: `myserver.duckdns.org` (or whatever you chose)

### Step 3: Set IP Address (30 seconds)

1. In the domain row, you'll see an IP field
2. Enter: `93.90.162.141`
3. Click **"Update IP"**

**Done!** Your domain is ready.

### Step 4: Tell Me Your Domain

Once you have your domain (e.g., `myserver.duckdns.org`), tell me and I'll update the configuration automatically!

Or you can update it yourself:
1. Edit `docker-compose.yml`
2. Find `# YOUR-DOMAIN.duckdns.org {`
3. Replace `YOUR-DOMAIN.duckdns.org` with your actual domain
4. Uncomment the lines (remove the `#`)

## Alternative: Try HTTPS with Public IP First

You can try using HTTPS with your public IP (may not work in Gmail due to self-signed cert):

```
https://93.90.162.141/resources/logo.png
```

But Gmail usually blocks self-signed certificates, so a free domain is the best solution.

