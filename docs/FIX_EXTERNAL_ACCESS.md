# Fix External Access Issues

## Quick Diagnosis

Run these commands on your server to diagnose the issue:

```bash
# 1. Check what's using port 80
sudo netstat -tlnp | grep :80
# or
sudo ss -tlnp | grep :80

# 2. Check if Nginx is running
sudo systemctl status nginx

# 3. Check firewall
sudo ufw status

# 4. Check Caddy container
docker ps | grep caddy
docker logs caddy-proxy --tail 20

# 5. Test local access
curl http://localhost/health
curl http://localhost:3000/health
```

## Most Common Issue: Nginx Blocking Port 80

If you see nginx in the port 80 check, stop it:

```bash
# Stop and disable nginx
sudo systemctl stop nginx
sudo systemctl disable nginx

# Restart Caddy
docker-compose restart caddy

# Verify
curl http://93.90.162.141/health
```

## Fix Firewall

If firewall is blocking ports:

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

## Verify Caddy is Listening

```bash
# Check if Caddy is listening on all interfaces
docker exec caddy-proxy netstat -tlnp | grep -E ':(80|443)'

# Should show:
# tcp  0  0 0.0.0.0:80  0.0.0.0:*  LISTEN
# tcp  0  0 0.0.0.0:443 0.0.0.0:*  LISTEN
```

## Test External Access

From another computer or using curl:

```bash
# Test HTTP
curl http://93.90.162.141/health

# Test HTTPS (ignore cert warning)
curl -k https://93.90.162.141/health

# Test logo
curl http://93.90.162.141/resources/logo.png
```

## If Still Not Working

1. **Check Docker port mapping:**
   ```bash
   docker ps | grep caddy
   # Should show: 0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
   ```

2. **Check server firewall (if using cloud provider):**
   - AWS: Check Security Groups
   - Google Cloud: Check Firewall Rules
   - Azure: Check Network Security Groups
   - DigitalOcean: Check Firewall settings

3. **Test from server itself:**
   ```bash
   curl http://93.90.162.141/health
   # If this works but external doesn't, it's a firewall issue
   ```

4. **Check Caddy logs:**
   ```bash
   docker logs caddy-proxy
   # Look for any errors
   ```

