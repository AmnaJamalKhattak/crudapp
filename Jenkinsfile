pipeline {
    agent {
        docker {
            image 'selenium/standalone-chrome'
            args '--network host'  // To allow container to access host network
        }
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                // Clean workspace before checkout
                cleanWs()
                git branch: 'main', url: 'https://github.com/AmnaJamalKhattak/crudapp.git'
            }
        }
        
        stage('Install Python Dependencies') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y python3-pip
                    cd crud-main/selenium_tests
                    pip3 install -r requirements.txt
                '''
            }
        }
        
        stage('Start Application') {
            steps {
                sh '''
                    cd crud-main
                    # Install Docker Compose if not present
                    apt-get install -y docker-compose
                    # Start the application
                    docker-compose -f docker-compose-part1.yml up -d
                    # Wait for services to be ready
                    sleep 30
                '''
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                dir('crud-main/selenium_tests') {
                    sh '''
                        # Create directory for test reports
                        mkdir -p test-reports
                        # Run tests with HTML report
                        python3 -m pytest test_user_management.py -v --html=test-reports/report.html
                    '''
                }
            }
            post {
                always {
                    // Archive the test reports
                    archiveArtifacts artifacts: 'crud-main/selenium_tests/test-reports/**/*'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'crud-main/selenium_tests/test-reports',
                        reportFiles: 'report.html',
                        reportName: 'Selenium Test Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            sh '''
                cd crud-main
                docker-compose -f docker-compose-part1.yml down || true
            '''
        }
        success {
            emailext(
                subject: '✅ Selenium Tests Passed',
                body: '''
                    All tests passed successfully!
                    
                    Check the detailed test report in Jenkins pipeline artifacts.
                    
                    Job: ${JOB_NAME}
                    Build Number: ${BUILD_NUMBER}
                    Build URL: ${BUILD_URL}
                ''',
                recipientProviders: [developers()],
                attachLog: true
            )
        }
        failure {
            emailext(
                subject: '❌ Selenium Tests Failed',
                body: '''
                    Some tests failed. Please review the pipeline logs and test report.
                    
                    Job: ${JOB_NAME}
                    Build Number: ${BUILD_NUMBER}
                    Build URL: ${BUILD_URL}
                    
                    Check the detailed test report in Jenkins pipeline artifacts.
                ''',
                recipientProviders: [developers()],
                attachLog: true
            )
        }
    }
}
