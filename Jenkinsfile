pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'python --version; exit 0'
            }
        }
    }
    post {
        always {
            sh 'This will always run'
        }
        success {
            sh 'This will run only if successful'
        }
        failure {
            sh 'This will run only if failed'
        }
        unstable {
            sh 'This will run only if the run was marked as unstable'
        }
        changed {
            sh 'This will run only if the state of the Pipeline has changed'
            sh 'For example, the Pipeline was previously failing but is now successful'
        }
    }
}