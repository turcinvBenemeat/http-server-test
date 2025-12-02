pipeline {
    // Agent to run the pipeline on
    agent { label 'agent-a' }

    // Global environment variables for this project
    environment {
        IMAGE_NAME     = "your-image-name"        // Example: "my-service"
        CONTAINER_NAME = "your-container-name"    // Example: "my-service"
        APP_PORT       = "3001"
        EMAIL_TO       = "your-email@example.com"
    }

    stages {

        stage("Prepare") {
            steps {
                script {
                    env.GIT_SHA = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()

                    env.IMAGE_TAG = "${IMAGE_NAME}:${env.GIT_SHA}"

                    echo "Git SHA: ${env.GIT_SHA}"
                    echo "Image tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage("Build image") {
            steps {
                sh """
                    docker build -t ${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                """
            }
        }

        stage("Test") {
            steps {
                sh """
                    docker run --rm \
                        -e GIT_SHA=${GIT_SHA} \
                        ${IMAGE_TAG} pytest tests/ -v
                """
            }
        }

        stage("Deploy") {
            steps {
                sh '''
                    # Detect available docker compose command
                    if docker-compose version > /dev/null 2>&1; then
                        COMPOSE_CMD="docker-compose"
                    elif docker compose version > /dev/null 2>&1; then
                        COMPOSE_CMD="docker compose"
                    else
                        echo "Installing docker-compose locally..."

                        COMPOSE_BIN="$WORKSPACE/docker-compose"
                        ARCH=$(uname -m)
                        OS=$(uname -s | tr '[:upper:]' '[:lower:]')

                        case "$ARCH" in
                            x86_64) ARCH="x86_64" ;;
                            aarch64|arm64) ARCH="aarch64" ;;
                            *) ARCH="x86_64" ;;
                        esac

                        curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-${OS}-${ARCH}" -o "${COMPOSE_BIN}"
                        chmod +x "${COMPOSE_BIN}"

                        export PATH="${WORKSPACE}:${PATH}"
                        COMPOSE_CMD="docker-compose"
                    fi

                    echo "Using compose: $COMPOSE_CMD"

                    # Stop and clean old containers
                    docker stop ${CONTAINER_NAME} caddy-proxy 2>/dev/null || true
                    docker rm   ${CONTAINER_NAME} caddy-proxy 2>/dev/null || true

                    $COMPOSE_CMD down --remove-orphans 2>/dev/null || true

                    docker network prune -f || true

                    # Deploy
                    GIT_SHA=$GIT_SHA $COMPOSE_CMD --project-directory "$WORKSPACE" up -d --build --remove-orphans

                    echo "Deployment complete."
                '''
            }
        }
    }

    post {

        always {
            echo "Pipeline finished."
        }

        failure {
            script {
                def cause     = currentBuild.getBuildCauses()[0]
                def startedBy = cause?.userName ?: cause?.shortDescription ?: "SCM change"
                def shortSha  = (env.GIT_SHA ?: "").take(7)

                mail(
                    to: EMAIL_TO,
                    subject: "[FAILURE] ${env.JOB_NAME} #${env.BUILD_NUMBER} – Started by ${startedBy}",
                    mimeType: "text/html",
                    body: """
<html>
  <body style="font-family: Arial, sans-serif;">
    <h2 style="color:#c0392b;">Build FAILED</h2>

    <p>Started by: <strong>${startedBy}</strong></p>

    <table cellpadding="4" cellspacing="0" border="0" style="border-collapse: collapse;">
      <tr><th align="left">Job</th>       <td>${env.JOB_NAME}</td></tr>
      <tr><th align="left">Build</th>     <td>${env.BUILD_NUMBER}</td></tr>
      <tr><th align="left">Branch</th>    <td>${env.GIT_BRANCH ?: "main"}</td></tr>
      <tr><th align="left">Git SHA</th>   <td>${shortSha}</td></tr>
      <tr><th align="left">Image</th>     <td>${env.IMAGE_TAG}</td></tr>
      <tr><th align="left">Node</th>      <td>${env.NODE_NAME}</td></tr>
      <tr><th align="left">Duration</th>  <td>${currentBuild.durationString.replace(" and counting", "")}</td></tr>
    </table>

    <p><strong>Console log:</strong> <a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a></p>

    <p style="font-size: 12px; color: #777; margin-top: 20px;">
      This message was sent automatically by Jenkins after a failed deployment.
    </p>
  </body>
</html>
"""
                )
            }

            echo "Pipeline failed."
        }

        success {
            script {
                def cause     = currentBuild.getBuildCauses()[0]
                def startedBy = cause?.userName ?: cause?.shortDescription ?: "SCM change"
                def shortSha  = (env.GIT_SHA ?: "").take(7)

                mail(
                    to: EMAIL_TO,
                    subject: "[SUCCESS] ${env.JOB_NAME} #${env.BUILD_NUMBER} – Started by ${startedBy}",
                    mimeType: "text/html",
                    body: """
<html>
  <body style="font-family: Arial, sans-serif;">
    <h2 style="color:#27ae60;">Build SUCCESSFUL</h2>

    <p>Started by: <strong>${startedBy}</strong></p>

    <table cellpadding="4" cellspacing="0" border="0" style="border-collapse: collapse;">
      <tr><th align="left">Job</th>       <td>${env.JOB_NAME}</td></tr>
      <tr><th align="left">Build</th>     <td>${env.BUILD_NUMBER}</td></tr>
      <tr><th align="left">Branch</th>    <td>${env.GIT_BRANCH ?: "main"}</td></tr>
      <tr><th align="left">Git SHA</th>   <td>${shortSha}</td></tr>
      <tr><th align="left">Image</th>     <td>${env.IMAGE_TAG}</td></tr>
      <tr><th align="left">Node</th>      <td>${env.NODE_NAME}</td></tr>
      <tr><th align="left">Duration</th>  <td>${currentBuild.durationString.replace(" and counting", "")}</td></tr>
    </table>

    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>

    <p style="font-size: 12px; color: #777; margin-top: 20px;">
      This message was sent automatically by Jenkins after a successful deployment.
    </p>
  </body>
</html>
"""
                )
            }

            echo "Pipeline succeeded. Deployed image tag: ${IMAGE_TAG}"
        }
    }
}