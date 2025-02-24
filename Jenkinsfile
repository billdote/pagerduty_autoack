pipeline {
  agent any

  triggers {
    pollSCM('H/5 * * * *')
  }

  environment {
    imageId = "pagerduty_autoack:latest"
    containerName = "py-pagerduty-autoack"
    REGEX = "test"
    QUERYINTERVAL = "200"
  }

  stages {
    stage('Git Checkout') {
      options { timeout(time: 30, unit: 'MINUTES') }
      steps {
        git branch: 'main', url: 'https://github.com/billdote/pagerduty_autoack.git'
      }
    }
    stage('Build') {
      options { timeout(time: 30, unit: 'MINUTES') }
      steps {
        script {
          docker.build("${env.imageId}")
        }
      }
    }
    stage('Test') {
      options { timeout(time: 30, unit: 'MINUTES') }
      steps {
        withCredentials([string(credentialsId: 'pagerduty_api_key', variable: 'API_KEY')]) {
          script {
            docker.image("${env.imageId}").withRun('-e API_KEY=${API_KEY}' +
                " -e REGEX=${env.REGEX}" + 
                " -e QUERYINTERVAL=${env.QUERYINTERVAL}" +
                " --init" + 
                " --name ${env.containerName}") {

              // sleep for 3 minutes to wait for script to run
              sleep(time: 180, unit: 'SECONDS')

              // get status of container
              def state = sh(script: 'docker inspect --format="{{.State.Status}}" "${containerName}" 2> /dev/null', returnStdout: true).trim()

              if (state == 'running') {
                sh 'docker logs "${containerName}"'
                echo "Container status is ${state}. Test passed."
              }   else {
                sh 'docker logs "${containerName}"'
                error('Container status is ${state}. Test failed.')
              }
            }
          }
        }
      }
    }
  }

  post {
    always {
      // remove docker image
      sh 'docker rmi "${imageId}"'
    }
    success {
      echo 'Pipeline completed successfully!'
    }
    failure {
      echo 'Pipeline failed.'
    }
  }
}
