def label = "yakir-slave-${UUID.randomUUID().toString()}"

podTemplate(label: label, cloud: 'kubernetes', containers: [
  containerTemplate(name: 'yakir-custom', image: 'sahkfox/jenkins-agent', ttyEnabled: true, command: 'cat'),
],
volumes: [
  hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
  // hostPathVolume(mountPath: '/root/.kube/config', hostPath: '/root/.kube/config-k3s'),
]
) {
  node (label) {
    stage('Prepare') {
        echo "1.Prepare Stage"
        checkout scm
        script {
            build_tag = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
            if (env.BRANCH_NAME != 'master') {
                build_tag = "${env.BRANCH_NAME}-${build_tag}"
            }
        }
    }
    stage('Test') {
        echo "2.Test Stage"
        container('yakir-custom') {
            sh "docker info"
        }
    }
    stage('Build') {
        container('yakir-custom') {
            echo "3.Build Docker Image Stage"
            sh "docker build -t yakir-harbor.yakir.com/yakir-test/jenkins-demo:${build_tag} ."
        }
    }
    stage('Publish') {
        container('yakir-custom') {
            echo "4.Push Docker Image Stage"
            withCredentials([usernamePassword(credentialsId: 'dockerHub', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
                sh "echo ${dockerHubPassword} |docker login -u ${dockerHubUser} --password-stdin https://yakir-harbor.yakir.com/"
                sh "docker push yakir-harbor.yakir.com/yakir-test/jenkins-demo:${build_tag}"
            }
        }
    }
    stage('Deploy') {
        container('yakir-custom') {
            echo "5. Deploy Stage"
            if (env.BRANCH_NAME == 'master') {
                input "确认要部署线上环境吗？"
            }
            sh "sed -i 's/<BUILD_TAG>/${build_tag}/' k8s.yaml"
            sh "sed -i 's/<BRANCH_NAME>/${env.BRANCH_NAME}/' k8s.yaml"
            sh "kubectl apply -f k8s.yaml"
        }
    }
  }
}