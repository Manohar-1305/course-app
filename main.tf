provider "aws" {
  region = "ap-south-1"
}

data "aws_availability_zones" "available" {}

resource "aws_vpc" "hosting_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "Hosting-VPC"
  }
}

# Create a Public Subnet in the first available AZ
resource "aws_subnet" "hosting_subnet" {
  vpc_id                  = aws_vpc.hosting_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "Hosting-Public-1"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "hosting_igw" {
  vpc_id = aws_vpc.hosting_vpc.id

  tags = {
    Name = "Hosting-IGW"
  }
}

# Create a Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.hosting_vpc.id

  tags = {
    Name = "Hosting-Public-RT"
  }
}

# Add a Route for Internet Access
resource "aws_route" "internet_access" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.hosting_igw.id
}

# Associate the Route Table with the Public Subnet
resource "aws_route_table_association" "public_subnet_assoc" {
  subnet_id      = aws_subnet.hosting_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Create a Security Group (Open to Everywhere)
resource "aws_security_group" "open_sg" {
  vpc_id = aws_vpc.hosting_vpc.id

  # Allow all inbound traffic (Not recommended for production)
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Open-SG"
  }
}

# # Fetch the existing IAM instance profile
# data "aws_iam_instance_profile" "s3-access-profile" {
#   name = "s3-access-profile"
# }

# Kubernetes instance - Jenkins
resource "aws_instance" "Jenkins" {
  ami                    = "ami-03bb6d83c60fc5f7c"
  instance_type          = "t2.medium"
  key_name               = "testing-dev-1"
  subnet_id              = aws_subnet.hosting_subnet.id
  vpc_security_group_ids = [aws_security_group.open_sg.id]
  user_data              = file("kube-containerd-install.sh")

  tags = {
    Name                               = "Jenkins"
    "kubernetes.io/cluster/kubernetes" = "owned"
  }
}

#Kubernetes instance - Sonarqube
resource "aws_instance" "Sonarqube" {
  ami                    = "ami-03bb6d83c60fc5f7c"
  instance_type          = "t2.medium"
  key_name               = "testing-dev-1"
  subnet_id              = aws_subnet.hosting_subnet.id
  vpc_security_group_ids = [aws_security_group.open_sg.id]
  user_data              = file("sonarqube.sh")

  tags = {
    Name                               = "Sonarqube"
    "kubernetes.io/cluster/kubernetes" = "owned"
  }
}

# # Kubernetes instance - Nexus
# resource "aws_instance" "nexus" {
#   ami                    = "ami-03bb6d83c60fc5f7c"
#   instance_type          = "t2.medium"
#   key_name               = "testing-dev-1"
#   subnet_id              = aws_subnet.hosting_subnet.id
#   vpc_security_group_ids = [aws_security_group.open_sg.id]

#   tags = {
#     Name                               = "nexus"
#     "kubernetes.io/cluster/kubernetes" = "owned"
#   }
# }

# Outputs for the public IPs
output "Jenkins_public_ip" {
  description = "The Public IP address of the Jenkins instance"
  value       = aws_instance.Jenkins.public_ip
}

output "Sonarqube_public_ip" {
  description = "The Public IP address of the Sonarqube instance"
  value       = aws_instance.Sonarqube.public_ip
}

# output "Nexus_public_ip" {
#   description = "The Public IP address of the Nexus instance"
#   value       = aws_instance.nexus.public_ip
# }
