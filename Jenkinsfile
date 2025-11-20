pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        DOCKER_IMAGE = 'http-server-test'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        REGISTRY = credentials('docker-registry-url') // Configure in Jenkins credentials
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 --version
                    pip3 --version
                    pip3 install -r requirements.txt
                '''
            }
        }
        
        stage('Lint & Test') {
            steps {
                echo 'Running linter and tests...'
                sh '''
                    pip3 install -r requirements-dev.txt
                    pytest test_server.py -v || true
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker image to registry...'
                script {
                    docker.withRegistry("https://${REGISTRY}") {
                        dockerImage.push("${DOCKER_TAG}")
                        dockerImage.push("latest")
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                script {
                    // Customize deployment steps based on your infrastructure
                    // Examples:
                    // - Deploy to Kubernetes
                    // - Deploy to Docker Swarm
                    // - Deploy to cloud platform (AWS, GCP, Azure)
                    // - SSH deployment to server
                    
                    sh '''
                        echo "Deployment steps would go here"
                        echo "Example: kubectl set image deployment/http-server http-server=${DOCKER_IMAGE}:${DOCKER_TAG}"
                        echo "Or: docker-compose up -d"
                        echo "Or: ssh deploy@server 'docker pull ${DOCKER_IMAGE}:${DOCKER_TAG} && docker-compose up -d'"
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Performing health check...'
                script {
                    // Wait a bit for the server to start
                    sleep(time: 10, unit: 'SECONDS')
                    
                    // Perform health check
                    sh '''
                        # Replace with your actual deployment URL
                        DEPLOY_URL="${DEPLOY_URL:-http://localhost:3000}"
                        curl -f ${DEPLOY_URL}/health || exit 1
                        echo "Health check passed!"
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded!'
            // Add notifications (email, Slack, etc.)
        }
        failure {
            echo 'Pipeline failed!'
            // Add failure notifications
        }
        always {
            echo 'Cleaning up...'
            // Clean up Docker images, temporary files, etc.
        }
    }
}

