pipeline {
    agent { label 'agent-a' }

    environment {
        IMAGE_NAME     = "http-server-test"
        CONTAINER_NAME = "http-server-test"
        APP_PORT       = "3000"
    }

    stages {
        stage('Build image') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:latest .
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    docker run --rm ${IMAGE_NAME}:latest pytest test_server.py -v
                """
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    docker rm -f ${CONTAINER_NAME} || true

                    docker run -d --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:${APP_PORT} \
                        --restart unless-stopped \
                        ${IMAGE_NAME}:latest
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
            echo 'Pipeline succeeded!'
        }
    }
}
