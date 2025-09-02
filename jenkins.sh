#!/bin/bash

# Define log file
LOG_FILE="$HOME/jenkins_install.log"
# Ensure the log directory exists and set permissions
touch "$LOG_FILE"
chmod 644 "$LOG_FILE"

# Redirect all output and errors to the log file
exec > >(tee -a "$LOG_FILE") 2>&1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log "Starting Jenkins installation process"

# Update package list
log "Updating package list..."
sudo apt update -y

# Install OpenJDK 21 JRE
log "Installing OpenJDK 21 JRE..."
sudo apt install -y openjdk-21-jre

# Download and add Jenkins key
log "Downloading Jenkins GPG key..."
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

# Add Jenkins repository
log "Adding Jenkins repository..."
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list >/dev/null

# Update package list again
log "Updating package list for Jenkins repository..."
sudo apt-get update -y

# Install Jenkins
log "Installing Jenkins..."
sudo apt-get install -y jenkins

# Install Docker
log "Installing Docker..."
sudo apt install -y docker.io
sudo chmod 666 /var/run/docker.sock

# Sudoers for Jenkins without password
log "Adding Jenkins user to sudoers..."
echo "jenkins ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/jenkins
sudo chmod 440 /etc/sudoers.d/jenkins
sudo visudo -c

# Install Trivy
log "Installing Trivy..."
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update -y
sudo apt-get install -y trivy

# SonarScanner
log "Installing SonarScanner..."
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
sudo apt install -y unzip
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
sudo mv sonar-scanner-5.0.1.3006-linux /opt/sonar-scanner
echo 'export PATH=$PATH:/opt/sonar-scanner/bin' >> ~/.bashrc
source ~/.bashrc

# Snyk
log "Installing Snyk CLI..."
curl -Lo snyk "https://static.snyk.io/cli/latest/snyk-linux"
chmod +x snyk
sudo mv snyk /usr/local/bin
snyk --version

log "Installing Node.js 18 and npm..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs npm
sudo npm install -g snyk-to-html

# SonarQube container
log "Running SonarQube container..."
docker run -d --name sonar -p 9000:9000 sonarqube:lts-community

log "Installation process completed successfully!"

sudo apt update -y && sudo apt upgrade -y

sudo snap install kubectl --classic

curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/

cat <<EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30000
        hostPort: 30000
      - containerPort: 30001
        hostPort: 30001
      - containerPort: 30002
        hostPort: 30002
      - containerPort: 30003
        hostPort: 30003
      - containerPort: 30004
        hostPort: 30004
      - containerPort: 30005
        hostPort: 30005
  - role: worker
  - role: worker
EOF

# Set permissions for kind-config.yaml
sudo chmod 644 kind-config.yaml
sudo chown $USER:$USER kind-config.yaml

sudo kind create cluster --name my-cluster --config kind-config.yaml
