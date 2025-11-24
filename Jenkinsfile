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
                    
                    # Stop and remove old containers
                    \$COMPOSE_CMD down || true
                    
                    # Deploy with docker compose (includes Caddy for HTTPS)
                    # GIT_SHA is passed via environment variable
                    GIT_SHA=${GIT_SHA} \$COMPOSE_CMD up -d --build
                    
                    # Show status
                    \$COMPOSE_CMD ps
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
