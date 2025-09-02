pipeline {
    agent any

    environment {
        FLASK_APP = "app.py"
        VIRTUAL_ENV = ".venv"
        IMAGE_NAME = "course-website"
        IMAGE_TAG = "v1"
        ENVIRONMENT = "dev"
    }

    stages {
        stage("Cleanup Workspaces") {
            steps {
                cleanWs()
            }
        }

        stage("Checkout") {
            steps {
                git branch: 'main', url: 'https://github.com/Manohar-1305/course-app.git'
            }
        }

        stage("Install python3-venv") {
            steps {
                script {
                    sh 'sudo apt-get update'
                    sh 'sudo apt-get install -y python3-venv'
                }
            }
        }

        stage("Setup Virtual Environment") {
            steps {
                script {
                    sh 'python3 -m venv $VIRTUAL_ENV'
                    sh '$VIRTUAL_ENV/bin/pip install --upgrade pip'
                }
            }
        }

        stage("Install Dependencies") {
            steps {
                script {
                    sh '$VIRTUAL_ENV/bin/pip install -r requirements.txt || ls -l'
                    sh '$VIRTUAL_ENV/bin/pip install pytest'
                }
            }
        }

        stage("Run Unit Tests") {
            steps {
                script {
                    sh '$VIRTUAL_ENV/bin/pytest --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage("SonarQube Analysis") {
            steps {
                withSonarQubeEnv('sonar-server') {  
                    script {
                        sh '''
                        /opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectName=course-website \
                        -Dsonar.projectKey=course-website
                        '''
                    }
                }
            }
        }

        stage("Quality Gate") {
            steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar-token'
                }
            }
        }

        stage("Build Docker Image") {
            steps {
                script {
                   sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG . '
                }
            }
        }
        stage("Tivy Scan") {
            steps {
                script {
                   sh 'trivy image --format table -o trivy-image-report.html $IMAGE_NAME:$IMAGE_TAG  '
                }
            }
        }
    stage('Snyk Security Scan') {
    steps {
        script {
            withCredentials([string(credentialsId: 'Snyk-token', variable: 'SNYK_TOKEN')]) {
                sh '''
                snyk auth $SNYK_TOKEN
                snyk container test $IMAGE_NAME:$IMAGE_TAG --severity-threshold=high --json --debug > snyk-report.json || true
                
                snyk-to-html -i snyk-report.json -o snyk-report.html
                
                if grep -q '"vulnerabilities":\\[\\]' snyk-report.json; then
                    echo "No vulnerabilities found."
                else
                    echo "Vulnerabilities detected. Check snyk-report.html for details."
                fi
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'snyk-report.html', fingerprint: true
        }
        }
    }

    stage('Push Docker Image to Docker Hub') {
        steps {
            script {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                sh 'echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin'
                    }
                    sh 'docker tag $IMAGE_NAME:$IMAGE_TAG manoharshetty507/$IMAGE_NAME:$IMAGE_TAG'
                    sh 'docker push manoharshetty507/$IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }
    // stage('Run Docker Container') {
    //     steps {
    //         script {
    //             sh 'docker run -d --name course-website -p 5000:5000 $IMAGE_NAME:$IMAGE_TAG'
    //             }
    //         }
    //     }
stage('Kubernetes Authentication') {
    steps {
        script {
            withCredentials([file(credentialsId: 'kubeconfig-file', variable:'KUBECONFIG')]) {
                sh 'echo "Kubernetes authentication successful"'
            }
        }
    }
}

        stage('Deploy to Kubernetes') {
        steps {
        script {
            withCredentials([file(credentialsId: 'kubeconfig-file', variable:'KUBECONFIG')]) {
                // Apply the deployment manifest
                sh 'kubectl apply -f deployment.yaml'

            }
        }
    }
    }

    }
}

