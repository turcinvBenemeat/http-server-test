# HTTP Server API

RESTful HTTP API server with FastAPI, Docker, and Jenkins CI/CD.

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api` - API information
- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get user by ID
- `POST /api/users` - Create user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user
- `GET /docs` - Swagger UI documentation

## Deployment

Automatically deployed via Jenkins CI/CD pipeline on push to `main` branch.

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run server
uvicorn app.server:app --reload --port 3000

# Run tests
pytest app/test_server.py -v
```

## Docker

```bash
# Build and start containers
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

## Testing

### Option 1: Local Testing (Without Docker)

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Start server
uvicorn app.server:app --reload --port 3000

# In another terminal, test endpoints:
curl http://localhost:3000/
curl http://localhost:3000/health
curl http://localhost:3000/api/users

# Or open in browser:
# http://localhost:3000/docs (Swagger UI)
```

### Option 2: Docker Testing

```bash
# Start containers
docker-compose up -d --build

# Wait a few seconds for containers to start, then test:
curl http://localhost/health
curl http://localhost/api/users

# Or access via HTTPS (self-signed cert, ignore warning):
curl -k https://localhost/health

# View logs
docker-compose logs -f http-server
docker-compose logs -f caddy
```

### Option 3: Test Deployed Server

After Jenkins deployment, test on your server:

```bash
# Replace with your server IP or domain
curl http://93.90.162.141/health
curl http://93.90.162.141/api/users
```

## API Examples

### Get API info
```bash
curl http://localhost:3000/
```

### Health check
```bash
curl http://localhost:3000/health
```

### Get all users
```bash
curl http://localhost:3000/api/users
```

### Get user by ID
```bash
curl http://localhost:3000/api/users/1
```

### Create user
```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Update user
```bash
curl -X PUT http://localhost:3000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe"}'
```

### Delete user
```bash
curl -X DELETE http://localhost:3000/api/users/1
```

## Interactive API Documentation

Open in browser:
- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

