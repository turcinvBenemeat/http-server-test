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
docker-compose up -d --build
```

