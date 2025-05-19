pipeline {
    agent any

    environment {
        PROJECT_NAME = "crudapp"
        COMPOSE_FILE = "docker-compose-part2.yml" // This should match your part 2 filename
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AmnaJamalKhattak/crudapp.git'
            }
        }

        stage('Stop Existing Containers') {
            steps {
                sh "docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_FILE} down"
            }
        }

        stage('Build and Run Docker Containers') {
            steps {
                sh "docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_FILE} up -d --build"
            }
        }
    }

    post {
        always {
            echo "Build finished"
        }
    }
}
