pipeline {
    agent any

    environment {
        APP_NAME = "nimbusops"
        DOCKER_IMAGE = "arundevops0047/NimbusOps"
        DOCKER_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = "nimbusops-container"

        GIT_REPO = "https://github.com/arunkumarmniloor-eng/NimbusOps.git"
        GIT_BRANCH = "main"

        DOCKERHUB_CREDENTIALS = "dockerhub-creds"
        KUBECONFIG_CREDENTIALS = "kubeconfig-file"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
            }
        }

        stage('Verify Files') {
            steps {
                sh '''
                    echo "Listing project files..."
                    pwd
                    ls -la
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKERHUB_CREDENTIALS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE

                        sed -i "s|IMAGE_PLACEHOLDER|${DOCKER_IMAGE}:${DOCKER_TAG}|g" k8s/deployment.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml

                        kubectl rollout status deployment/nimbusops
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        kubectl get pods
                        kubectl get svc
                        kubectl get deployment
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "NimbusOps pipeline completed successfully."
        }

        failure {
            echo "NimbusOps pipeline failed. Check logs for details."
        }

        always {
            sh 'docker logout || true'
        }
    }
}
