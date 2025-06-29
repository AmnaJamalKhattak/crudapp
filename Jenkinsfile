pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'selenium-test-runner'
        DOCKER_CONTAINER = 'selenium-test-container'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clean workspace before checking out
                cleanWs()
                // Checkout code from Git
                checkout scm
            }
        }

        stage('Build Test Image') {
            steps {
                script {
                    // Build Docker image for running tests
                    sh '''
                        cd selenium_tests
                        docker build -t ${DOCKER_IMAGE} .
                    '''
                }
            }
        }

        stage('Start Application') {
            steps {
                script {
                    // Start the application containers
                    sh '''
                        docker-compose -f docker-compose-part1.yml up -d
                        # Wait for services to be ready
                        sleep 30
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        // Run tests in Docker container
                        sh '''
                            docker run --name ${DOCKER_CONTAINER} \
                                --network host \
                                ${DOCKER_IMAGE}
                        '''
                    } finally {
                        // Always stop and remove the test container
                        sh '''
                            docker stop ${DOCKER_CONTAINER} || true
                            docker rm ${DOCKER_CONTAINER} || true
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker resources
            script {
                sh '''
                    docker-compose -f docker-compose-part1.yml down
                    docker rmi ${DOCKER_IMAGE} || true
                '''
            }
        }
        success {
            echo 'Tests completed successfully!'
        }
        failure {
            echo 'Tests failed! Check the logs for details.'
        }
    }
}
