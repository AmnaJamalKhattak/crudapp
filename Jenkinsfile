pipeline {
    agent any

    environment {
        PROJECT_NAME = "crudapp"  // Your project name here
        COMPOSE_FILE = "docker-compose.yml"  // Assuming docker-compose.yml is in repo root
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AmnaJamalKhattak/crudapp.git'
            }
        }

        stage('Build Docker Containers') {
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
