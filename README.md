# HTTP Server with Jenkins CI/CD

A RESTful HTTP API server built with Python FastAPI and automated deployment via Jenkins CI/CD pipeline.

## Features

- RESTful API with FastAPI
- Automatic API documentation (Swagger UI at `/docs`)
- Health check endpoint
- User CRUD operations
- Docker containerization
- Jenkins CI/CD pipeline
- Automated testing with pytest
- Type validation with Pydantic

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /api` - API information
- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get user by ID
- `POST /api/users` - Create new user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Prerequisites

- Python 3.11+
- pip or conda
- Docker (for containerized deployment)
- Jenkins server

## Local Development

### Option 1: Using Conda (Recommended)

1. Create or update conda environment:
```bash
# If environment doesn't exist, create it:
conda env create -f environment.yml

# If environment already exists, update it:
conda env update -n test -f environment.yml --prune

# OR using mamba (faster):
mamba env update -n test -f environment.yml --prune

# For development environment (includes test dependencies)
conda env create -f environment-dev.yml
# or update existing:
conda env update -n test-dev -f environment-dev.yml --prune
```

2. Activate the environment:
```bash
conda activate test
# or for development
conda activate test-dev
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Start the server:
```bash
python server.py
# or using uvicorn directly
uvicorn server:app --reload --port 3000
```

### Option 2: Using venv

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Start the server:
```bash
python server.py
# or using uvicorn directly
uvicorn server:app --reload --port 3000
```

5. Test the API:
```bash
curl http://localhost:3000/health
curl http://localhost:3000/api
```

6. View API documentation:
- Swagger UI: http://localhost:3000/docs
- ReDoc: http://localhost:3000/redoc

## Docker Deployment

### Build and run with Docker:
```bash
docker build -t http-server-test .
docker run -p 3000:3000 http-server-test
```

### Using Docker Compose:
```bash
docker-compose up -d
```

## Jenkins Setup

### 1. Install Required Jenkins Plugins

- Pipeline
- Docker Pipeline
- Git

### 2. Configure Jenkins Credentials

1. Go to Jenkins → Manage Jenkins → Credentials
2. Add credentials for:
   - Docker registry (if using private registry)
   - SSH keys (if deploying via SSH)
   - Any other required credentials

### 3. Create Jenkins Pipeline Job

1. Create a new Pipeline job in Jenkins
2. Configure the pipeline:
   - **Pipeline definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your Git repository URL
   - **Branch**: `*/main` (or your default branch)
   - **Script Path**: `Jenkinsfile`

### 4. Customize Jenkinsfile

Edit the `Jenkinsfile` to match your deployment infrastructure:

- **Docker Registry**: Update `REGISTRY` environment variable
- **Deployment Steps**: Customize the `Deploy` stage based on your infrastructure:
  - Kubernetes: Use `kubectl` commands
  - Docker Swarm: Use `docker stack deploy`
  - Cloud Platform: Use platform-specific CLI tools
  - SSH Deployment: Use SSH commands to deploy to your server

### 5. Environment Variables

Set these in Jenkins job configuration or Jenkinsfile:
- `DEPLOY_URL`: Your deployment URL for health checks
- `DOCKER_REGISTRY`: Your Docker registry URL
- Any other environment-specific variables

## Deployment Options

### Option 1: Docker Compose Deployment

If deploying to a server with Docker Compose:

```groovy
stage('Deploy') {
    steps {
        sh '''
            ssh deploy@your-server.com << EOF
                cd /path/to/app
                docker-compose pull
                docker-compose up -d
            EOF
        '''
    }
}
```

### Option 2: Kubernetes Deployment

```groovy
stage('Deploy') {
    steps {
        sh '''
            kubectl set image deployment/http-server \
                http-server=${DOCKER_IMAGE}:${DOCKER_TAG} \
                -n production
            kubectl rollout status deployment/http-server -n production
        '''
    }
}
```

### Option 3: Direct Docker Deployment

```groovy
stage('Deploy') {
    steps {
        sh '''
            ssh deploy@your-server.com << EOF
                docker pull ${DOCKER_IMAGE}:${DOCKER_TAG}
                docker stop http-server || true
                docker rm http-server || true
                docker run -d --name http-server \
                    -p 3000:3000 \
                    --restart unless-stopped \
                    ${DOCKER_IMAGE}:${DOCKER_TAG}
            EOF
        '''
    }
}
```

## Testing

Run tests:
```bash
pytest test_server.py -v
```

Run tests with coverage:
```bash
pytest test_server.py --cov=server --cov-report=html
```

## Project Structure

```
.
├── server.py              # Main server file (FastAPI application)
├── requirements.txt       # Production dependencies (pip)
├── requirements-dev.txt   # Development dependencies (pip)
├── environment.yml        # Conda environment (production)
├── environment-dev.yml    # Conda environment (development)
├── test_server.py         # Test suite
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose configuration
├── Jenkinsfile            # Jenkins CI/CD pipeline
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Environment Variables

- `PORT`: Server port (default: 3000)
- `NODE_ENV`: Environment (development/production)

## API Examples

### Create a user:
```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Get all users:
```bash
curl http://localhost:3000/api/users
```

### Get user by ID:
```bash
curl http://localhost:3000/api/users/1
```

### Update user:
```bash
curl -X PUT http://localhost:3000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe"}'
```

### Delete user:
```bash
curl -X DELETE http://localhost:3000/api/users/1
```

## License

MIT
# Auto deploy test Thu Nov 20 14:32:48 CET 2025
