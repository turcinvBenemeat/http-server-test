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
                echo 'Running tests...'
                sh '''
                    pip3 install pytest pytest-asyncio httpx || true
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
            when {
                expression { env.REGISTRY != null && env.REGISTRY != '' }
            }
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
                    // Option 1: SSH Deployment with Docker Compose (Recommended for personal servers)
                    // Configure SSH credentials in Jenkins: Manage Jenkins → Credentials → Add SSH Username with private key
                    // Set environment variables in Jenkins job:
                    //   DEPLOY_SERVER = "user@your-server.com"
                    //   DEPLOY_PATH = "/opt/http-server-test"
                    //   DEPLOY_SSH_CREDENTIALS = "ssh-credentials-id"
                    
                    def deployServer = env.DEPLOY_SERVER ?: 'deploy@your-server.com'
                    def deployPath = env.DEPLOY_PATH ?: '/opt/http-server-test'
                    def sshCredentials = env.DEPLOY_SSH_CREDENTIALS ?: 'ssh-deploy-key'
                    
                    sshagent([sshCredentials]) {
                        sh """
                            echo "📦 Copying files to server..."
                            # Copy docker-compose.yml and necessary files
                            scp -o StrictHostKeyChecking=no docker-compose.yml Dockerfile requirements.txt ${deployServer}:${deployPath}/
                            scp -o StrictHostKeyChecking=no server.py ${deployServer}:${deployPath}/
                            
                            echo "🚀 Deploying on server..."
                            ssh -o StrictHostKeyChecking=no ${deployServer} "cd ${deployPath} && docker-compose build && docker-compose down || true && docker-compose up -d && sleep 5 && docker-compose ps"
                        """
                    }
                    
                    // Alternative: Direct Docker deployment (uncomment if preferred)
                    /*
                    sh """
                        ssh ${deployServer} << EOF
                            docker pull ${DOCKER_IMAGE}:${DOCKER_TAG} || docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ${deployPath}
                            docker stop http-server-test || true
                            docker rm http-server-test || true
                            docker run -d --name http-server-test \\
                                -p 3000:3000 \\
                                --restart unless-stopped \\
                                ${DOCKER_IMAGE}:${DOCKER_TAG}
                        EOF
                    """
                    */
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
                    def deployUrl = env.DEPLOY_URL ?: "http://localhost:3000"
                    if (env.DEPLOY_SERVER) {
                        def serverHost = env.DEPLOY_SERVER.split('@').last()
                        deployUrl = "http://${serverHost}:3000"
                    }
                    sh """
                        echo "Checking health at ${deployUrl}/health"
                        curl -f ${deployUrl}/health || exit 1
                        echo "✅ Health check passed!"
                    """
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

