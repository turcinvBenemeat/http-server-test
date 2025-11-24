pipeline {
    agent { label 'agent-a' }

    environment {
        IMAGE_NAME     = "http-server-test"
        CONTAINER_NAME = "http-server-test"
        APP_PORT       = "3000"
    }

    stages {
        stage('Prepare') {
            steps {
                script {
                    env.GIT_SHA = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.IMAGE_TAG = "${IMAGE_NAME}:${env.GIT_SHA}"
                    echo "Git SHA: ${env.GIT_SHA}"
                    echo "Image tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Build image') {
            steps {
                sh """
                    docker build -t ${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    docker run --rm \
                        -e GIT_SHA=${GIT_SHA} \
                        ${IMAGE_TAG} pytest app/test_server.py -v --rootdir=/app
                """
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    # Detect which docker compose command is available
                    if docker-compose version > /dev/null 2>&1; then
                        COMPOSE_CMD="docker-compose"
                    elif docker compose version > /dev/null 2>&1; then
                        COMPOSE_CMD="docker compose"
                    else
                        echo "Neither 'docker-compose' nor 'docker compose' is available"
                        echo "Installing docker-compose to workspace directory..."
                        
                        # Install to workspace directory (user-writable)
                        COMPOSE_BIN="\${WORKSPACE}/docker-compose"
                        ARCH=\$(uname -m)
                        OS=\$(uname -s | tr '[:upper:]' '[:lower:]')
                        
                        # Map architecture names
                        case "\$ARCH" in
                            x86_64) ARCH="x86_64" ;;
                            aarch64|arm64) ARCH="aarch64" ;;
                            *) ARCH="x86_64" ;;
                        esac
                        
                        curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-\${OS}-\${ARCH}" -o "\${COMPOSE_BIN}"
                        chmod +x "\${COMPOSE_BIN}"
                        
                        # Add to PATH for this session
                        export PATH="\${WORKSPACE}:\${PATH}"
                        COMPOSE_CMD="docker-compose"
                        
                        echo "Installed docker-compose to \${COMPOSE_BIN}"
                    fi
                    
                    echo "Using: \$COMPOSE_CMD"
                    
                    # Force stop and remove containers (even if not managed by compose)
                    echo "Stopping and removing existing containers..."
                    docker stop http-server-test caddy-proxy 2>/dev/null || true
                    docker rm http-server-test caddy-proxy 2>/dev/null || true
                    
                    # Stop and remove containers via docker-compose (if they exist)
                    \$COMPOSE_CMD down --remove-orphans 2>/dev/null || true
                    
                    # Clean up any orphaned networks
                    docker network prune -f || true
                    
                    # Ensure config directory and Caddyfile exist
                    echo "Verifying config files..."
                    pwd
                    echo "Current directory contents:"
                    ls -la
                    echo "Checking config directory:"
                    ls -la config/ || echo "config directory does not exist, creating..."
                    mkdir -p config
                    
                    if [ ! -f config/Caddyfile ]; then
                        echo "ERROR: config/Caddyfile not found!"
                        echo "Available files in config/:"
                        ls -la config/ || echo "config directory is empty"
                        echo "Checking if file exists with absolute path..."
                        ls -la \${WORKSPACE}/config/Caddyfile || echo "Absolute path also not found"
                        echo "Checking git status..."
                        git status config/Caddyfile || echo "File not in git"
                        exit 1
                    fi
                    
                    echo "Caddyfile found, verifying it's a file (not directory)..."
                    [ -f config/Caddyfile ] && echo "✓ Caddyfile is a file" || echo "✗ Caddyfile is not a file"
                    [ -d config/Caddyfile ] && echo "✗ ERROR: Caddyfile is a directory!" && exit 1
                    echo "Caddyfile contents (first 5 lines):"
                    head -5 config/Caddyfile || echo "Could not read Caddyfile"
                    
                    # Change to workspace directory to ensure relative paths work
                    cd \${WORKSPACE}
                    echo "Changed to workspace: \$(pwd)"
                    echo "Verifying Caddyfile path:"
                    ls -la config/Caddyfile
                    echo "Caddyfile size: \$(stat -c%s config/Caddyfile 2>/dev/null || stat -f%z config/Caddyfile 2>/dev/null || echo 'unknown') bytes"
                    
                    # Check if it's actually a symlink or special file
                    echo "File type details:"
                    ls -l config/Caddyfile
                    readlink config/Caddyfile 2>/dev/null || echo "Not a symlink"
                    
                    # Create absolute path for Caddyfile
                    CADDYFILE_PATH="\$(realpath config/Caddyfile || echo \${WORKSPACE}/config/Caddyfile)"
                    echo "Absolute Caddyfile path: \${CADDYFILE_PATH}"
                    
                    # Temporarily modify docker-compose.yml to use absolute path
                    # Backup original
                    cp docker-compose.yml docker-compose.yml.bak
                    # Replace relative path with absolute path
                    sed -i "s|\\./config/Caddyfile|\${CADDYFILE_PATH}|g" docker-compose.yml
                    echo "Updated docker-compose.yml:"
                    grep Caddyfile docker-compose.yml
                    
                    # Deploy with docker compose (includes Caddy for HTTPS)
                    # GIT_SHA is passed via environment variable
                    echo "Deploying containers..."
                    GIT_SHA=${GIT_SHA} \$COMPOSE_CMD --project-directory \${WORKSPACE} up -d --build --remove-orphans
                    
                    # Restore original docker-compose.yml
                    mv docker-compose.yml.bak docker-compose.yml || true
                    
                    # Wait a moment for containers to start
                    sleep 5
                    
                    # Show status
                    echo "Container status:"
                    \$COMPOSE_CMD ps
                    
                    # Show logs for debugging
                    echo "Recent logs:"
                    \$COMPOSE_CMD logs --tail=20
                """
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
        }
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo "Pipeline succeeded! Deployed image tag: ${IMAGE_TAG}"
        }
    }
}
