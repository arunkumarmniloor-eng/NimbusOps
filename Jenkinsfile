pipeline {
    agent any

    environment {
        APP_NAME = "nimbusops"
        DOCKER_IMAGE = "arundevops0047/nimbusops"
        DOCKER_TAG = "${BUILD_NUMBER}"
        GIT_REPO = "https://github.com/arunkumarmniloor-eng/NimbusOps.git"
        GIT_BRANCH = "main"
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

        stage('Build Docker Image') {
            steps {
                bat """
                    docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% .
                    docker tag %DOCKER_IMAGE%:%DOCKER_TAG% %DOCKER_IMAGE%:latest
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                bat """
                    docker push %DOCKER_IMAGE%:%DOCKER_TAG%
                    docker push %DOCKER_IMAGE%:latest
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat """
                    kubectl apply -f k8s\\deployment.yaml
                    kubectl apply -f k8s\\service.yaml
                    kubectl get pods
                    kubectl get svc
                """
            }
        }
    }

    post {
        success {
            echo 'NimbusOps pipeline completed successfully.'
        }
        failure {
            echo 'NimbusOps pipeline failed.'
        }
    }
}
