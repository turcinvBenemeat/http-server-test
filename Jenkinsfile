pipeline {
    agent { label 'agent-a' }

    environment {
        IMAGE_NAME     = "http-server-test"
        CONTAINER_NAME = "http-server-test"
        APP_PORT       = "3001"
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
                    
                    # Deploy with docker compose (includes Caddy for HTTPS)
                    # GIT_SHA is passed via environment variable
                    echo "Deploying containers..."
                    GIT_SHA=${GIT_SHA} \$COMPOSE_CMD --project-directory \${WORKSPACE} up -d --build --remove-orphans
                    
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
            mail(
                to: 'turcinv@btlnet.com',
                subject: "[SUCCESS] ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build SUCCESSFUL.

Job:        ${env.JOB_NAME}
Build:      ${env.BUILD_NUMBER}
Git SHA:    ${env.GIT_SHA}
Image tag:  ${env.IMAGE_TAG}
Node:       ${env.NODE_NAME}
URL:        ${env.BUILD_URL}

This message was sent automatically by Jenkins after a successful deployment.
"""
            )
            echo "Pipeline succeeded! Deployed image tag: ${IMAGE_TAG} (success email sent)"
        }
    }
}
