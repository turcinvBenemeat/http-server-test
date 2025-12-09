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

        stage('Approval') {
            steps {
                script {
                    // Send email asking for approval
                    mail(
                        to: 'turcinv@btlnet.com',
                        subject: "[APPROVAL NEEDED] ${env.JOB_NAME} #${env.BUILD_NUMBER} – Git SHA ${env.GIT_SHA}",
                        mimeType: 'text/html',
                        body: """
<html>
  <body style=\"font-family: Arial, sans-serif;\">
    <h2 style=\"color:#2980b9;\">Deployment approval required</h2>

    <p>The build <strong>${env.JOB_NAME} #${env.BUILD_NUMBER}</strong> finished successfully and is waiting for deployment approval.</p>

    <table cellpadding=\"4\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse; font-size:14px;\">
      <tr>
        <th align=\"left\">Branch</th>
        <td>${env.GIT_BRANCH ?: 'main'}</td>
      </tr>
      <tr>
        <th align=\"left\">Git SHA</th>
        <td>${env.GIT_SHA}</td>
      </tr>
      <tr>
        <th align=\"left\">Image tag</th>
        <td>${env.IMAGE_TAG}</td>
      </tr>
    </table>

    <p style=\"margin-top:16px;\">
      To approve the deployment, open Jenkins and click <strong>Proceed</strong> on the input step for this build:<br/>
      <a href=\"${env.BUILD_URL}\">${env.BUILD_URL}</a>
    </p>

    <p style=\"margin-top:8px; font-size:12px; color:#777;\">
      If you do not approve within the timeout window, the deployment will be cancelled automatically.
    </p>
  </body>
</html>
"""
                    )

                    // Wait for manual approval in Jenkins UI (linked in the email above)
                    timeout(time: 1, unit: 'HOURS') {
                        input message: 'Approve deployment to production?', ok: 'Deploy'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    # Detect which docker compose command is available
                    if docker-compose version > /dev/null 2>&1; then
                        COMPOSE_CMD="docker-compose"
                    elif docker compose version > /dev/null 2>&1; then
                        COMPOSE_CMD="docker compose"
                    else
                        echo "Neither 'docker-compose' nor 'docker compose' is available"
                        echo "Installing docker-compose to workspace directory..."

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

                        echo "Installed docker-compose to ${COMPOSE_BIN}"
                    fi

                    echo "Using: $COMPOSE_CMD"

                    echo "Stopping and removing existing containers..."
                    docker stop http-server-test caddy-proxy 2>/dev/null || true
                    docker rm http-server-test caddy-proxy 2>/dev/null || true

                    $COMPOSE_CMD down --remove-orphans 2>/dev/null || true

                    docker network prune -f || true

                    echo "Deploying containers..."
                    GIT_SHA=$GIT_SHA $COMPOSE_CMD --project-directory "$WORKSPACE" up -d --build --remove-orphans

                    sleep 5

                    echo "Container status:"
                    $COMPOSE_CMD ps

                    echo "Recent logs:"
                    $COMPOSE_CMD logs --tail=20
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
        }

        failure {
            script {
                def cause     = currentBuild.getBuildCauses()[0]
                def startedBy = cause?.userName ?: cause?.shortDescription ?: 'SCM change'
                def shortSha  = (env.GIT_SHA ?: '').take(7)

                mail(
                    to: 'turcinv@btlnet.com',
                    subject: "[FAILURE] ${env.JOB_NAME} #${env.BUILD_NUMBER} – started by ${startedBy}",
                    mimeType: 'text/html',
                    body: """
<html>
  <body style="font-family: Arial, sans-serif;">
    <h2 style="color:#c0392b;">Build FAILED</h2>

    <p>Started by: <strong>${startedBy}</strong></p>

    <table cellpadding="4" cellspacing="0" border="0" style="border-collapse:collapse; font-size:14px;">
      <tr>
        <th align="left">Job</th>
        <td>${env.JOB_NAME}</td>
      </tr>
      <tr>
        <th align="left">Build</th>
        <td>${env.BUILD_NUMBER}</td>
      </tr>
      <tr>
        <th align="left">Branch</th>
        <td>${env.GIT_BRANCH ?: 'main'}</td>
      </tr>
      <tr>
        <th align="left">Git SHA</th>
        <td>${shortSha}</td>
      </tr>
      <tr>
        <th align="left">Image tag</th>
        <td>${env.IMAGE_TAG}</td>
      </tr>
      <tr>
        <th align="left">Node</th>
        <td>${env.NODE_NAME}</td>
      </tr>
      <tr>
        <th align="left">Duration</th>
        <td>${currentBuild.durationString.replace(' and counting', '')}</td>
      </tr>
    </table>

    <p style="margin-top:16px;">
      <strong>Console log:</strong>
      <a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a>
    </p>

    <hr style="margin-top:20px; border:none; border-top:1px solid #ddd;" />
    <p style="font-size:12px; color:#777;">
      This message was sent automatically by Jenkins after a failed deployment.
    </p>
  </body>
</html>
"""
                )
            }
            echo 'Pipeline failed!'
        }

        success {
            script {
                def cause     = currentBuild.getBuildCauses()[0]
                def startedBy = cause?.userName ?: cause?.shortDescription ?: 'SCM change'
                def shortSha  = (env.GIT_SHA ?: '').take(7)

                mail(
                    to: 'turcinv@btlnet.com',
                    subject: "[SUCCESS] ${env.JOB_NAME} #${env.BUILD_NUMBER} – started by ${startedBy}",
                    mimeType: 'text/html',
                    body: """
<html>
  <body style="font-family: Arial, sans-serif;">
    <h2 style="color:#27ae60;">Build SUCCESSFUL</h2>

    <p>Started by: <strong>${startedBy}</strong></p>

    <table cellpadding="4" cellspacing="0" border="0" style="border-collapse:collapse; font-size:14px;">
      <tr>
        <th align="left">Job</th>
        <td>${env.JOB_NAME}</td>
      </tr>
      <tr>
        <th align="left">Build</th>
        <td>${env.BUILD_NUMBER}</td>
      </tr>
      <tr>
        <th align="left">Branch</th>
        <td>${env.GIT_BRANCH ?: 'main'}</td>
      </tr>
      <tr>
        <th align="left">Git SHA</th>
        <td>${shortSha}</td>
      </tr>
      <tr>
        <th align="left">Image tag</th>
        <td>${env.IMAGE_TAG}</td>
      </tr>
      <tr>
        <th align="left">Node</th>
        <td>${env.NODE_NAME}</td>
      </tr>
      <tr>
        <th align="left">Duration</th>
        <td>${currentBuild.durationString.replace(' and counting', '')}</td>
      </tr>
    </table>

    <p style="margin-top:16px;">
      <strong>Build URL:</strong>
      <a href="${env.BUILD_URL}">${env.BUILD_URL}</a>
    </p>

    <hr style="margin-top:20px; border:none; border-top:1px solid #ddd;" />
    <p style="font-size:12px; color:#777;">
      This message was sent automatically by Jenkins after a successful deployment.
    </p>
  </body>
</html>
"""
                )
            }
            echo "Pipeline succeeded! Deployed image tag: ${IMAGE_TAG} (success email sent)"
        }
    }
}
